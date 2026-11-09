"""Lecturas acotadas de recursos; no señales ni cambios de servicios."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import time
import os

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
p.add_argument('--stop', required=True)
p.add_argument('--seconds', type=int, default=3600)
a = p.parse_args()
base = Path('/home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa')
ids = ['cerebro-consultable-20261109','workshop-kit-piloto-20261109','fabrica-lector-panel-20261109']

def proc(pid, expected=None):
    try:
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        if fields[0] == 'Z':
            return None
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        if expected and boot + ':' + fields[19] != expected:
            return None
        return {'pid': pid, 'ppid': int(fields[1]), 'start': fields[19], 'cpu_ticks': int(fields[11]) + int(fields[12]),
                'rss_bytes': int(fields[21]) * os.sysconf('SC_PAGE_SIZE')}
    except (OSError, ValueError, IndexError):
        return None

previous = None
previous_procs = {}
previous_time = None
end = time.monotonic() + a.seconds
with Path(a.output).open('x') as out:
    while time.monotonic() < end and not Path(a.stop).exists():
        mem = {line.split(':')[0]: int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines() if line.split(':')[0] in ['MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree']}
        vmstat = {line.split()[0]: int(line.split()[1]) for line in Path('/proc/vmstat').read_text().splitlines() if line.split()[0] in ('pswpin','pswpout','oom_kill')}
        pressure = {name:(Path('/proc/pressure')/name).read_text().strip() for name in ('cpu','memory','io')}
        cpu = list(map(int, Path('/proc/stat').read_text().splitlines()[0].split()[1:9]))
        busy = None
        if previous:
            total = sum(cpu) - sum(previous)
            idle = cpu[3] + cpu[4] - previous[3] - previous[4]
            busy = round(100 * (total - idle) / total, 2) if total else None
        previous = cpu
        sample_time = time.monotonic()
        all_procs = {}
        for path in Path('/proc').iterdir():
            if path.name.isdecimal():
                value = proc(int(path.name))
                if value:
                    all_procs[value['pid']] = value
        live = []
        for ident in ids:
            row = json.loads((base / '04-operacion-agentes/tareas' / (ident + '.json')).read_text())
            for session in row.get('sesiones', []):
                processes = []
                for key, start in [('pid', 'pid_inicio'), ('supervisor_pid', 'supervisor_inicio')]:
                    if session.get(key):
                        result = proc(session[key], session.get(start))
                        if result:
                            processes.append(result)
                if processes:
                    owned = {v['pid'] for v in processes}
                    while True:
                        added = {v['pid'] for v in all_procs.values() if v['ppid'] in owned} - owned
                        if not added:
                            break
                        owned |= added
                    tree = [all_procs[pid] for pid in owned if pid in all_procs]
                    delta = sum(max(0, v['cpu_ticks'] - previous_procs.get((v['pid'], v['start']), v['cpu_ticks'])) for v in tree)
                    pct = None if previous_time is None else round(100 * delta / os.sysconf('SC_CLK_TCK') / (sample_time - previous_time) / os.cpu_count(), 3)
                    live.append({'id': ident, 'intento': session['intento'], 'rol': session['rol'], 'procesos': tree,
                        'rss_arbol_bytes': sum(v['rss_bytes'] for v in tree), 'cpu_pct_capacidad_host_arbol': pct})
        out.write(json.dumps({'fecha_utc': datetime.now(timezone.utc).isoformat(), 'cpu_ocupada_pct_host': busy,
            'memoria_kib_host': mem, 'vmstat':vmstat, 'pressure':pressure, 'sesiones_principales_vivas': live,
            'limites': 'Árboles PPID observados, sin procesos ya terminados/reparentados; RSS suma memoria compartida varias veces. CPU normalizada por cores del host. No es cuota del modelo.'}) + '\n')
        out.flush()
        previous_procs = {(v['pid'], v['start']): v['cpu_ticks'] for v in all_procs.values()}
        previous_time = sample_time
        time.sleep(5)
