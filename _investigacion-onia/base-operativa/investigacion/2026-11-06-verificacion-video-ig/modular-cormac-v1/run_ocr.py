import csv,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREFIX=ROOT.parents[2]/'operacion/modular-cormac-v1/tesseract'
ref=ROOT/'ocr-reference.json'
assert hashlib.sha256(ref.read_bytes()).hexdigest()=='e0a4b2ee8534ee0d310d612567487062df80ebf49d68714bbb1b33a79b2fd43b'
references=json.loads(ref.read_bytes());selection=json.loads((ROOT/'crop-selection.json').read_bytes())
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(PREFIX/'usr/lib/x86_64-linux-gnu')
env['TESSDATA_PREFIX']=str(next(PREFIX.rglob('eng.traineddata')).parent)
freeze={'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'configuration':{'language':'eng','oem':1,'psm':7,'rescaling':False},'crops':[]}
for r in references:
    crop=ROOT/f"crop-{r['case']}.png";sha=hashlib.sha256(crop.read_bytes()).hexdigest();assert sha==r['crop_sha256']
    freeze['crops'].append({'case':r['case'],'sha256':sha})
with (ROOT/'ocr-input-freeze.json').open('x')as f:json.dump(freeze,f,indent=2);f.write('\n')
results=[]
for r in references:
    case=r['case'];crop=ROOT/f'crop-{case}.png';out=ROOT/f'ocr-{case}'
    command=[str(PREFIX/'usr/bin/tesseract'),str(crop),str(out),'-l','eng','--oem','1','--psm','7','-c','tessedit_create_tsv=1','-c','tessedit_create_txt=1']
    subprocess.run(command,env=env,check=True)
    raw=out.with_suffix('.txt').read_text();text=' '.join(raw.split());expect=' '.join(r['expected_text'].split())
    rect=next(x['rect_xywh']for x in selection['cases']if x['case']==case)
    words=[]
    with out.with_suffix('.tsv').open()as f:
        for row in csv.DictReader(f,delimiter='\t'):
            if row['level']=='5' and row['text'].strip():
                words.append({'text':row['text'],'confidence':float(row['conf']),'crop_rect':[int(row[k])for k in ['left','top','width','height']],'source_rect':[rect[0]+int(row['left']),rect[1]+int(row['top']),int(row['width']),int(row['height'])]})
    results.append({'case':case,'expected':r['expected_text'],'reference_legibility':r['legibility'],'raw':raw,'text':text,'literal_match_whitespace_collapsed':text==expect,'casefold_match':text.casefold()==expect.casefold(),'words':words,'command':command})
(ROOT/'ocr-results.json').write_text(json.dumps({'results':results,'reference_frozen_before_execution':True,'confidence_is_not_calibrated_probability':True},indent=2)+'\n')
print(json.dumps(results))
