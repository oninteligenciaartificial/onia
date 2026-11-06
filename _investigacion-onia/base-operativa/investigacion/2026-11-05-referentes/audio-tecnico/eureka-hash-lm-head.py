"""SHA-256 exacto de tres tensores BF16 sin cargar el modelo en RAM."""
import hashlib
import json
import struct
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MODEL=BASE/'operacion/referentes-20261105/audio/eureka-preflight'
index=json.loads((MODEL/'model.safetensors.index.json').read_text(encoding='utf-8'))['weight_map']
keys=['lm_head.weight','backbone.lm_head.weight','backbone.model.embed_tokens.weight']
rows=[]
for key in keys:
    path=MODEL/index[key]
    with path.open('rb') as f:
        length=struct.unpack('<Q',f.read(8))[0]
        header=json.loads(f.read(length))
        item=header[key]
        start,end=item['data_offsets']
        f.seek(8+length+start)
        left=end-start
        h=hashlib.sha256()
        while left:
            data=f.read(min(left,1024*1024))
            if not data: raise EOFError(key)
            h.update(data); left-=len(data)
    rows.append({'key':key,'shard':path.name,'dtype':item['dtype'],'shape':item['shape'],
                 'bytes':end-start,'sha256':h.hexdigest()})
result={'scope':'bytes completos de tres tensores de checkpoint; no prueba alias runtime',
        'equal_all':len({r['sha256'] for r in rows})==1,'tensors':rows}
(OUT/'eureka-lm-head-hashes.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
