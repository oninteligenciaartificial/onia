"""Offline static validation of retained official bytes; no prefix assumptions."""
from pathlib import Path
import csv,io,json,hashlib
O=Path(__file__).resolve().parent;p=O/'class_labels_indices.raw.csv';b=p.read_bytes();rows=list(csv.DictReader(io.StringIO(b.decode())))
assert len(rows)==527 and list(rows[0])==['index','mid','display_name']
assert [int(x['index']) for x in rows]==list(range(527)) and len({x['mid'] for x in rows})==527
assert all(x['mid'] and x['display_name'] for x in rows)
assert sum(x['display_name']=='Speech' for x in rows)==1 and sum(x['display_name']=='Music' for x in rows)==1
sha=hashlib.sha256(b).hexdigest();dest=O.parent/'panns-setup-v3/runtime-home/panns_data/class_labels_indices.csv'
with open(dest,'xb') as f:f.write(b)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
receipt={'complete':True,'source':json.loads((O/'csv-receipt.json').read_text())['fixed_URL'],'generation':'1488737428851815','bytes':len(b),'sha256':sha,'rows':527,'unique_mids':527,'columns':list(rows[0]),'mid_namespaces_observed':sorted({x['mid'].split('/')[1] for x in rows}),'Speech_index':int(next(x['index'] for x in rows if x['display_name']=='Speech')),'Music_index':int(next(x['index'] for x in rows if x['display_name']=='Music')),'installed_path':str(dest),'network_requests':0,'code_or_global_HOME_changed':False,'prior_validation_failures':'overstrict invented namespace assumptions, preserved separately; raw fixed-generation bytes reused without another request'}
(O/'csv-installed.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
