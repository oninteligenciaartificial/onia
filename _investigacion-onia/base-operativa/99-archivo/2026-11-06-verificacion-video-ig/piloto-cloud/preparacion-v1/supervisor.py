"""Linux/stdlib supervisor. Local cooperative children, NOT a security sandbox.

AS/CPU are per-process inherited rlimits, not RSS or aggregate group quotas.
Resource guards and RSS are sampled. A child that escapes the session is outside
this monitor: do not use with untrusted programs or permit daemonization.
"""
import argparse
import dataclasses
import json
import math
import os
from pathlib import Path
import resource
import selectors
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path('/workspace/onia-av-pilot-20261106')
GIB = 1024 ** 3
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')


@dataclasses.dataclass(frozen=True)
class Policy:
    as_bytes: int = 12 * GIB
    cpu_seconds: int = 600
    wall_seconds: float = 600
    threads: int = 2
    affinity_count: int = 2
    reserve_bytes: int = 8 * GIB
    disk_free_bytes: int = 30 * GIB
    tree_bytes: int = 16 * GIB
    interval: float = 0.1
    log_bytes: int = 256 * 1024
    output_bytes: int = 1024 * 1024


def validate(p):
    for name in ('as_bytes', 'cpu_seconds', 'threads', 'affinity_count',
                 'reserve_bytes', 'disk_free_bytes', 'tree_bytes', 'log_bytes', 'output_bytes'):
        if type(getattr(p, name)) is not int or getattr(p, name) <= 0:
            raise ValueError('invalid positive integer: ' + name)
    if not (16 * 1024**2 <= p.as_bytes <= 12 * GIB):
        raise ValueError('AS must be 16 MiB..12 GiB')
    if p.cpu_seconds > 600 or not math.isfinite(p.wall_seconds) or not 0 < p.wall_seconds <= 600:
        raise ValueError('CPU/wall must be <=600 seconds')
    if p.threads != 2 or p.affinity_count != 2:
        raise ValueError('two threads/two affinity CPUs required')
    if p.reserve_bytes < 8 * GIB or p.disk_free_bytes < 30 * GIB or p.tree_bytes > 16 * GIB:
        raise ValueError('resource guard weakened')
    if not math.isfinite(p.interval) or not 0.02 <= p.interval <= 0.5:
        raise ValueError('sampling interval outside 0.02..0.5 s')
    if not p.log_bytes <= p.output_bytes <= 1024 * 1024:
        raise ValueError('output must be <=1 MiB and log <= output')
    cpus = sorted(os.sched_getaffinity(0))[:2]
    if len(cpus) != 2:
        raise ValueError('fewer than two available CPUs')
    for kind, value in ((resource.RLIMIT_AS, p.as_bytes), (resource.RLIMIT_CPU, p.cpu_seconds)):
        hard = resource.getrlimit(kind)[1]
        if hard != resource.RLIM_INFINITY and hard < value:
            raise ValueError('inherited hard limit is smaller than requested')
    return cpus


def cgroup_levels():
    """Discover actual unified mount and walk all namespace-visible ancestors."""
    group = next(line.split(':', 2)[2] for line in Path('/proc/self/cgroup').read_text().splitlines()
                 if line.startswith('0::'))
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        before, after = line.split(' - ', 1)
        if after.split()[0] != 'cgroup2':
            continue
        fields = before.split()
        mount_root, mount = fields[3], Path(fields[4])
        if group != mount_root and not group.startswith(mount_root.rstrip('/') + '/'):
            continue
        leaf = mount / group[len(mount_root):].lstrip('/')
        levels = []
        while True:
            maximum = (leaf / 'memory.max').read_text().strip()
            current = int((leaf / 'memory.current').read_text())
            levels.append({'path': str(leaf), 'max': maximum, 'current': current})
            if leaf == mount:
                return levels
            leaf = leaf.parent
    raise RuntimeError('readable cgroup v2 memory hierarchy required')


def tree_size(root):
    total = 0
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            try:
                total += os.lstat(Path(directory) / name).st_size
            except FileNotFoundError:
                pass  # concurrent deletion
    return total


def snapshot(root):
    available = next(int(line.split()[1]) * 1024
                     for line in Path('/proc/meminfo').read_text().splitlines()
                     if line.startswith('MemAvailable:'))
    levels = cgroup_levels()
    headrooms = [max(0, int(x['max']) - x['current']) for x in levels if x['max'] != 'max']
    if not headrooms:
        raise RuntimeError('no visible finite cgroup memory.max; cannot confirm reserve')
    return {'mem_available': available, 'cgroups': levels,
            'reserve': min(available, *headrooms),
            'disk_free': shutil.disk_usage(root).free, 'tree_bytes': tree_size(root)}


def guard(s, p):
    if s['reserve'] < p.reserve_bytes:
        return 'memory_reserve'
    if s['disk_free'] < p.disk_free_bytes:
        return 'disk_reserve'
    if s['tree_bytes'] > p.tree_bytes:
        return 'tree_limit'
    return None


def group_sample(pgid):
    members = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            tail = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(tail[2]) == pgid and int(tail[3]) == pgid:
                members.append({'pid': int(entry.name), 'state': tail[0],
                                'rss_bytes': int(tail[21]) * os.sysconf('SC_PAGE_SIZE'),
                                'threads': int(tail[17]),
                                'affinity': sorted(os.sched_getaffinity(int(entry.name)))})
        except (OSError, ValueError, IndexError):
            continue
    return members


def kill_own_group(child):
    # PGID is the leader PID allocated by start_new_session=True, never caller's.
    if child.pid <= 1 or child.pid == os.getpgrp():
        raise RuntimeError('refusing unsafe PGID')
    members = group_sample(child.pid)
    if members:
        os.killpg(child.pid, signal.SIGKILL)
    return [m['pid'] for m in members]


def launch_child(spec_path):
    spec = json.loads(Path(spec_path).read_text())
    p = Policy(**spec['policy'])
    validate(p)
    # This code executes in a new session/process, never in the agent or parent.
    os.sched_setaffinity(0, spec['cpus'])
    resource.setrlimit(resource.RLIMIT_AS, (p.as_bytes, p.as_bytes))
    resource.setrlimit(resource.RLIMIT_CPU, (p.cpu_seconds, p.cpu_seconds))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    for key in THREAD_KEYS:
        os.environ[key] = '2'
    effective = {'pid': os.getpid(), 'pgid': os.getpgrp(), 'sid': os.getsid(0),
                 'rlimit_as': resource.getrlimit(resource.RLIMIT_AS),
                 'rlimit_cpu': resource.getrlimit(resource.RLIMIT_CPU),
                 'affinity': sorted(os.sched_getaffinity(0)), 'thread_settings': dict.fromkeys(THREAD_KEYS, '2'),
                 'thread_limit_scope': 'library settings, not a kernel thread-count quota'}
    with open(spec['effective_file'], 'x') as out:
        json.dump(effective, out)
    os.chdir(spec['cwd'])
    os.execvpe(spec['command'][0], spec['command'], os.environ)


def run(command, run_name, policy=None):
    p = policy or Policy()
    cpus = validate(p)  # all validation before spawning
    root = ROOT.resolve(strict=True)
    if root != ROOT or not root.is_dir() or root.stat().st_uid != os.getuid():
        raise ValueError('expected owned, non-symlink workspace')
    if not command or any(not isinstance(x, str) or '\0' in x for x in command):
        raise ValueError('invalid argv')
    if not run_name or not all(c.isalnum() or c in '-_' for c in run_name):
        raise ValueError('invalid run name')
    run_dir = root / ('run-' + run_name)
    run_dir.mkdir()  # no overwrite/resume of previous evidence
    try:
        initial = snapshot(root)
        why = guard(initial, p)
        (run_dir / 'preflight.json').write_text(json.dumps({'resources': initial, 'rejected': why}, indent=2)+'\n')
        if why:
            raise RuntimeError('preflight: ' + why)
    except BaseException as exc:
        (run_dir / 'preflight-failure.json').write_text(json.dumps({'error': type(exc).__name__+': '+str(exc)})+'\n')
        raise
    spec = {'command': command, 'policy': dataclasses.asdict(p), 'cpus': cpus,
            'cwd': str(run_dir), 'effective_file': str(run_dir / 'effective.json')}
    spec_path = run_dir / 'spec.json'
    spec_path.write_text(json.dumps(spec, indent=2) + '\n')
    parent_before = {'as': resource.getrlimit(resource.RLIMIT_AS),
                     'cpu': resource.getrlimit(resource.RLIMIT_CPU),
                     'affinity': sorted(os.sched_getaffinity(0))}
    report = {'command': command, 'policy': dataclasses.asdict(p), 'initial': initial,
              'parent_before': parent_before, 'reason': None, 'sample_count': 0,
              'sampled_max_group_rss_bytes': 0, 'sampled_max_single_rss_bytes': 0,
              'rss_scope': 'sum of observed group RSS; shared pages may be counted twice; not exact peak',
              'output_seen_bytes': 0, 'log_written_bytes': 0,
              'limits_scope': 'AS and CPU per process; guards sampled; visible cgroup ancestors only',
              'thread_scope': 'library settings=2, sampled per-process thread count <=2; no kernel thread quota',
              'killed_members': []}
    child = None
    started = time.monotonic()
    try:
        child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--child', str(spec_path)],
                                 start_new_session=True, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        report['pgid'] = child.pid
        selector = selectors.DefaultSelector()
        selector.register(child.stdout, selectors.EVENT_READ)
        with open(run_dir / 'output.log', 'xb') as log, open(run_dir / 'samples.jsonl', 'x') as samples:
            while True:
                ready = (run_dir / 'effective.json').is_file()
                members = group_sample(child.pid)
                s = snapshot(root)
                rss = sum(m['rss_bytes'] for m in members)
                report['sample_count'] += 1
                report['sampled_max_group_rss_bytes'] = max(report['sampled_max_group_rss_bytes'], rss)
                report['sampled_max_single_rss_bytes'] = max(report['sampled_max_single_rss_bytes'], max((m['rss_bytes'] for m in members), default=0))
                samples.write(json.dumps({'elapsed': time.monotonic()-started, 'members': members, 'resources': s})+'\n')
                report['last_snapshot'] = s
                report['reason'] = guard(s, p)
                if ready and any(m['threads'] > p.threads for m in members):
                    report['reason'] = 'thread_count_limit'
                if ready and any(not set(m['affinity']).issubset(cpus) for m in members):
                    report['reason'] = 'affinity_changed'
                if not ready and time.monotonic() - started > 2:
                    report['reason'] = 'child_setup_timeout'
                if time.monotonic() - started >= p.wall_seconds:
                    report['reason'] = 'wall_timeout'
                if report['reason']:
                    break
                for key, _ in selector.select(p.interval):
                    data = os.read(key.fd, 65536)
                    if not data:
                        selector.unregister(key.fileobj)
                    report['output_seen_bytes'] += len(data)
                    keep = data[:max(0, p.log_bytes-report['log_written_bytes'])]
                    log.write(keep)
                    report['log_written_bytes'] += len(keep)
                if report['output_seen_bytes'] > p.output_bytes:
                    report['reason'] = 'output_limit'
                    break
                if child.poll() is not None:
                    # Capture remaining bounded data, then remove any group descendants.
                    for _ in range(17):
                        if not selector.select(0):
                            break
                        data = os.read(child.stdout.fileno(), 65536)
                        if not data:
                            break
                        report['output_seen_bytes'] += len(data)
                        keep = data[:max(0, p.log_bytes-report['log_written_bytes'])]
                        log.write(keep)
                        report['log_written_bytes'] += len(keep)
                    if report['output_seen_bytes'] > p.output_bytes:
                        report['reason'] = 'output_limit'
                    break
        selector.close()
    except BaseException as exc:
        report['reason'] = 'supervisor_exception'
        report['exception'] = type(exc).__name__ + ': ' + str(exc)
    finally:
        if child is not None:
            try:
                report['killed_members'] = kill_own_group(child)
            except ProcessLookupError:
                pass
            report['exit_code'] = child.wait(timeout=5)
            child.stdout.close()
        effective_path = run_dir / 'effective.json'
        report['effective'] = json.loads(effective_path.read_text()) if effective_path.exists() else None
        report['elapsed_seconds'] = time.monotonic() - started
        report['parent_after'] = {'as': resource.getrlimit(resource.RLIMIT_AS),
                                  'cpu': resource.getrlimit(resource.RLIMIT_CPU),
                                  'affinity': sorted(os.sched_getaffinity(0))}
        report['parent_limits_unchanged'] = report['parent_before'] == report['parent_after']
        report['log_truncated'] = report['output_seen_bytes'] > report['log_written_bytes']
        if report['reason'] is None:
            report['reason'] = 'exited' if report.get('exit_code') == 0 else 'child_failure'
        (run_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--child':
        launch_child(sys.argv[2])
    else:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--name', required=True)
        parser.add_argument('command', nargs=argparse.REMAINDER)
        args = parser.parse_args()
        cmd = args.command[1:] if args.command[:1] == ['--'] else args.command
        result = run(cmd, args.name)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result['reason'] == 'exited' else 1)
