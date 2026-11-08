"""Coteja selección pública de pistas: etiqueta MP4 'eng' no prueba idioma real."""
import json
import re
import subprocess
from pathlib import Path
from recuperar_youtube import COMMON,IDS

OUT=Path(__file__).resolve().parent
rows=[]
for vid in IDS:
    cmd=COMMON+['--skip-download','--dump-single-json','--format',
        'bv*[height<=720][vcodec^=avc1]+ba/b[height<=720]/bv*[height<=720]+ba',
        'https://www.youtube.com/watch?v='+vid]
    p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',timeout=120)
    row={'id':vid,'metadata_exit':p.returncode,'stderr':p.stderr}
    if p.returncode==0:
        data=json.loads(p.stdout)
        row['current_selection']=[{k:f.get(k) for k in ['format_id','language','language_preference','format_note','acodec','vcodec']} for f in data.get('requested_formats',[])]
        log=OUT/(vid+('-media-download.log' if vid in IDS[:4] else '-download.log'))
        match=re.search(r'Downloading 1 format\(s\): (.+)',log.read_text(encoding='utf-8'))
        row['downloaded_format_ids']=match.group(1).strip() if match else None
        row['current_format_ids']=data.get('format_id')
        row['same_selection_ids']=row['downloaded_format_ids']==row['current_format_ids']
    rows.append(row)
    (OUT/'idiomas-pistas.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(row,ensure_ascii=True),flush=True)
