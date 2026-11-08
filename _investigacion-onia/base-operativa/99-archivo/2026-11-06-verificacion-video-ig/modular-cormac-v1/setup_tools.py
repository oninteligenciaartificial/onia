"""Download official APT packages into a private prefix; never install globally."""
import hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREFIX=ROOT.parents[2]/'operacion/modular-cormac-v1/tesseract'
PREFIX.mkdir(parents=True,exist_ok=False)
pool=PREFIX/'packages';pool.mkdir()
packages=['tesseract-ocr','tesseract-ocr-eng','libtesseract5','libleptonica6']
records=[]
for package in packages:
    raw=subprocess.check_output(['apt-cache','show','--no-all-versions',package],text=True)
    fields=dict(line.split(': ',1) for line in raw.splitlines() if ': ' in line and not line.startswith(' '))
    records.append({'package':package,'version':fields['Version'],'expected_sha256':fields['SHA256'],'repository_file':fields['Filename']})
subprocess.run(['apt-get','download']+[r['package']+'='+r['version'] for r in records],cwd=pool,check=True)
for archive in pool.glob('*.deb'):
    package=subprocess.check_output(['dpkg-deb','-f',str(archive),'Package'],text=True).strip()
    record=next(r for r in records if r['package']==package)
    record['sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert record['sha256']==record['expected_sha256']
    record['bytes']=archive.stat().st_size
    subprocess.run(['dpkg-deb','-x',str(archive),str(PREFIX)],check=True)
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(PREFIX/'usr/lib/x86_64-linux-gnu')
env['TESSDATA_PREFIX']=str(PREFIX/'usr/share/tesseract-ocr/5/tessdata')
check=subprocess.run([str(PREFIX/'usr/bin/tesseract'),'--version'],env=env,capture_output=True,text=True)
report={'prefix':str(PREFIX),'packages':records,'version_exit':check.returncode,'version_output':check.stdout+check.stderr,'global_install':False,'admin':False}
(ROOT/'tools-receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
if check.returncode: raise RuntimeError('isolated tesseract dependency unresolved; see receipt')
