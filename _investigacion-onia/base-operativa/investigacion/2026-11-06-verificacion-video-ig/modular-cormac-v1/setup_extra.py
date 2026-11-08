import hashlib,json,os,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=ROOT.parents[2]/'operacion/modular-cormac-v1/tesseract'
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(P/'usr/lib/x86_64-linux-gnu')
mapping={'libarchive.so.13':'libarchive13t64','libjpeg.so.8':'libjpeg-turbo8','libgif.so.7':'libgif7','libtiff.so.6':'libtiff6','libxml2.so.16':'libxml2-16','libnettle.so.8':'libnettle8t64','libjbig.so.0':'libjbig0','libLerc.so.4':'liblerc4','libdeflate.so.0':'libdeflate0','libwebp.so.7':'libwebp7','libsharpyuv.so.0':'libsharpyuv0'}
records=[]
for iteration in range(3):
    raw=subprocess.run(['ldd',str(P/'usr/bin/tesseract')],env=env,capture_output=True,text=True).stdout
    missing=sorted(set(re.findall(r'^\s*(\S+) => not found',raw,re.M)))
    if not missing:break
    for soname in missing:
        package=mapping[soname]
        meta=subprocess.check_output(['apt-cache','show','--no-all-versions',package],text=True)
        fields=dict(line.split(': ',1)for line in meta.splitlines()if ': 'in line and not line.startswith(' '))
        subprocess.run(['apt-get','download',package+'='+fields['Version']],cwd=P/'packages',check=True)
        archive=next(a for a in (P/'packages').glob('*.deb') if subprocess.check_output(['dpkg-deb','-f',str(a),'Package'],text=True).strip()==package)
        sha=hashlib.sha256(archive.read_bytes()).hexdigest();assert sha==fields['SHA256']
        subprocess.run(['dpkg-deb','-x',str(archive),str(P)],check=True)
        records.append({'package':package,'version':fields['Version'],'bytes':archive.stat().st_size,'sha256':sha,'expected_sha256':fields['SHA256']})
r=subprocess.run([str(P/'usr/bin/tesseract'),'--version'],env=env,capture_output=True,text=True)
report={'extra_dependencies':records,'exit_code':r.returncode,'version':r.stdout+r.stderr,'global_install':False,'traineddata':[str(x.relative_to(P))for x in P.rglob('eng.traineddata')]}
(ROOT/'tools-extra-receipt.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert r.returncode==0
