"""Auditoría de artefactos, no nueva generación ni evaluación de calidad."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMES = ['general','desarrollo','automatizaciones','organizacion','aprendizaje','marketing','video','producto']
IDS = {'general':'g','desarrollo':'d','automatizaciones':'a','organizacion':'o','aprendizaje':'l','marketing':'m','video':'v','producto':'p'}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def records(obj):
    if isinstance(obj,list):
        for x in obj: yield from records(x)
    elif isinstance(obj,dict):
        if 'sha256' in obj: yield obj
        else:
            for v in obj.values(): yield from records(v)
results=[]
for name in NAMES:
    d=ROOT/f'caso-{name}'
    config=read(d/'configuracion-previa.json')
    arms=[]
    for a in ['brazo-01','brazo-02']:
        folder=d/a
        rec=read(folder/'lectura.json')
        checks=[]
        for item in records(rec):
            label=next((item[k] for k in ['ruta','fuente','archivo','path'] if k in item),None)
            if not label: checks.append({'error':'source name missing'}); continue
            p=Path(label)
            if not p.is_absolute(): p=d/label
            checks.append({'source':str(p),'match':p.exists() and sha(p)==str(item['sha256']).lower()})
        expected_count = (5 if name=='desarrollo' else 4 if name=='producto' else 3) + (0 if a=='brazo-01' else 5 if name=='video' else 3 if name=='producto' else 1)
        arms.append({'arm':a,'agent':'/root/'+IDS[name]+a[-2:],
                     'requested_model':'gpt-6.1-terra' if name in ['desarrollo','automatizaciones','producto'] else 'gpt-6.1-sol',
                     'effort':'medium','fork':'none',
                     'raw_sha256':sha(folder/'artefacto.raw.md'),
                     'receipt_sha256':sha(folder/'lectura.json'),
                     'receipt_before_artifact':(folder/'lectura.json').stat().st_mtime_ns <= (folder/'artefacto.raw.md').stat().st_mtime_ns,
                     'source_checks':checks,'expected_sources':expected_count,'source_count_matches':len(checks)==expected_count})
    mapping=read(d/'mapa-ciego.json')
    blind=[]
    for label in ['X','Y']:
        raw=d/mapping[label]/'artefacto.raw.md'
        p=d/'ciego'/f'{label}.md'
        blind.append({'label':label,'identical_to_raw':sha(raw)==sha(p),'sha256':sha(p)})
    frozen=read(d/'congelacion.json') if (d/'congelacion.json').exists() else config
    entries=frozen.get('archivos',frozen.get('fixture',[]))
    fixture_checks=[{'file':x['ruta'],'match':sha(d/x['ruta'])==x['sha256']} for x in entries]
    if name=='desarrollo':
        fixture_checks += [{'file':a+'/'+f,'match':sha(d/a/f)==sha(d/f)} for a in ['brazo-01','brazo-02'] for f in ['fixture.py','check_funcional.py']]
    results.append({'case':name,'arms':arms,'blind':blind,'frozen':fixture_checks,'judge_id':'/root/j'+IDS[name],
                    'judge_saved':(d/'ciego'/'juicio.json').exists(), 'judge_sha256':sha(d/'ciego'/'juicio.json') if (d/'ciego'/'juicio.json').exists() else None})
output={'scope':'lectura declarada con hashes y artefactos; no certifica memoria interna ni ausencia absoluta de herramientas no registradas',
        'cases':8,'arms':16,'repeats':0,'max_worker_generations_concurrent':3,'results':results}
(ROOT/'caso-general'/'auditoria-piloto.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf-8')
bad=[(x['case'],a['arm'],c) for x in results for a in x['arms'] for c in a['source_checks'] if not c.get('match',False)]
print(json.dumps({'source_hash_failures':bad,'source_count_mismatch':[(x['case'],a['arm'],len(a['source_checks']),a['expected_sources']) for x in results for a in x['arms'] if not a['source_count_matches']],'frozen_failures':[x['case'] for x in results if not all(c['match'] for c in x['frozen'])],
                  'blind_changed':[x['case'] for x in results if not all(c['identical_to_raw'] for c in x['blind'])],
                  'receipts_after_raw':[(x['case'],a['arm']) for x in results for a in x['arms'] if not a['receipt_before_artifact']],
                  'judges_saved':sum(x['judge_saved'] for x in results)},ensure_ascii=False))
