"""Read-only resource inventory; no credentials, environment dumps or mutations."""
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess

memory = {}
for line in Path('/proc/meminfo').read_text().splitlines():
    key, value = line.split(':', 1)
    if key in {'MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'}:
        memory[key + '_bytes'] = int(value.split()[0]) * 1024
disk = os.statvfs('/')
result = {
    'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'read_only',
    'cpu_logical': os.cpu_count(),
    'load_averages': os.getloadavg(),
    'memory': memory,
    'root_disk_available_bytes': disk.f_bavail * disk.f_frsize,
    'nvidia_device_present': Path('/dev/nvidia0').exists(),
    'nvidia_smi_available': shutil.which('nvidia-smi') is not None,
    'ffmpeg_available': shutil.which('ffmpeg') is not None,
    'cmake_available': shutil.which('cmake') is not None,
    'cxx_available': shutil.which('g++') is not None,
}
pilot = Path('/opt/onia-referentes-media/cormac-01/DfWLWspIruU.mp4')
try:
    result['existing_cormac_original_bytes'] = pilot.stat().st_size
except OSError as exc:
    result['existing_cormac_original_access'] = type(exc).__name__
if shutil.which('docker'):
    run = subprocess.run(['docker', 'ps', '-a', '--format', '{{.Names}}\t{{.Status}}'], capture_output=True, text=True, timeout=10)
    result['docker_list_exit'] = run.returncode
    if run.returncode == 0:
        rows = [line.split('\t', 1) for line in run.stdout.splitlines()]
        result['containers_total'] = len(rows)
        result['own_pilots'] = [row for row in rows if row[0].startswith(('onia-asr-pilot-', 'onia-audio-'))]
    else:
        result['docker_list_error'] = 'Permission denied or daemon unavailable; no escalation attempted.'
print(json.dumps(result, ensure_ascii=True, indent=2))
