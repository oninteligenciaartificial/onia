"""Read-only storage measurement; writes only its JSON receipt in this workspace."""
from pathlib import Path
import datetime
import json
import os
import shutil
import stat

ROOT=Path('/workspace/onia-av-pilot-20261106')
OUT=ROOT/'resume-negativo-v1'
verified={str((ROOT/'negativo-v1/weights'/x['path']).relative_to(ROOT)) for x in json.loads((OUT/'weights-receipt.json').read_bytes())['verified']}
names=('weights_complete_verified','weights_partial_or_unverified','runtime_code',
       'build_cmake','controls','logs_receipts_zip')
groups={name:{'file_apparent_bytes':0,'allocated_blocks_bytes':0,'files':0,
              'symlink_apparent_bytes':0,'symlinks':0} for name in names}
seen=set();duplicates=0;directory_apparent=0;directory_blocks=0
def category(relative):
    name=relative.as_posix()
    if name.startswith('negativo-v1/weights/'):
        return 'weights_complete_verified' if name in verified else 'weights_partial_or_unverified'
    if name.startswith('negativo-v1/signals/'): return 'controls'
    if name.startswith(('runtime/','__pycache__/')): return 'runtime_code'
    if name.startswith(('build-v2/','cmake-local/')) or name=='cmake-4.4.4.whl': return 'build_cmake'
    if relative.suffix.lower() in ('.json','.jsonl','.log','.zip'): return 'logs_receipts_zip'
    return 'runtime_code'
for directory,dirs,files in os.walk(ROOT,followlinks=False):
    dirs.sort();files.sort()
    ds=os.lstat(directory);directory_apparent+=ds.st_size;directory_blocks+=ds.st_blocks*512
    entries=files+[name for name in dirs if (Path(directory)/name).is_symlink()]
    for name in entries:
        path=Path(directory)/name;s=path.lstat();key=(s.st_dev,s.st_ino)
        if key in seen: duplicates+=1;continue
        seen.add(key);g=groups[category(path.relative_to(ROOT))]
        if stat.S_ISLNK(s.st_mode):
            g['symlinks']+=1;g['symlink_apparent_bytes']+=s.st_size
        elif stat.S_ISREG(s.st_mode):g['files']+=1;g['file_apparent_bytes']+=s.st_size
        else:continue
        g['allocated_blocks_bytes']+=s.st_blocks*512
file_total=sum(g['file_apparent_bytes'] for g in groups.values())
link_total=sum(g['symlink_apparent_bytes'] for g in groups.values())
blocks_total=sum(g['allocated_blocks_bytes'] for g in groups.values())
disk=shutil.disk_usage(ROOT)
result={'measured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':str(ROOT),'categories':groups,'directory_metadata_apparent_bytes':directory_apparent,
        'directory_metadata_allocated_blocks_bytes':directory_blocks,
        'total_file_apparent_bytes':file_total,'total_symlink_apparent_bytes':link_total,
        'total_apparent_including_directory_metadata_bytes':file_total+link_total+directory_apparent,
        'total_allocated_blocks_including_directory_metadata_bytes':blocks_total+directory_blocks,
        'hardlink_duplicate_entries_not_double_counted':duplicates,
        'symlink_policy':'lstat link storage only; never follow/count target twice',
        'blocks_scope':'st_blocks*512 reported by this filesystem, not exclusive host billing or provisioned capacity',
        'workspace_filesystem_total_bytes':disk.total,'workspace_filesystem_free_bytes':disk.free,
        'ram_and_cgroup':'separate memory-observation.json; not storage',
        'persistence':'observed between turns only; NOT permanent storage'}
(OUT/'inventory-storage.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'apparent_total':result['total_apparent_including_directory_metadata_bytes'],
                  'allocated_blocks_total':result['total_allocated_blocks_including_directory_metadata_bytes'],
                  'disk_free':disk.free}))
