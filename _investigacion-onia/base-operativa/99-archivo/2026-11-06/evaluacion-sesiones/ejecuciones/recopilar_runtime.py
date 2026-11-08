from pathlib import Path
import json, hashlib, sys
logs=Path(r'C:\Users\PC\.codex\sessions\2026\11\06')
parent='01a1b245-bfe7-70f1-a4a1-a8c6eed15b4a'
base=Path(r'C:\dev\proyectos\_investigacion-onia\base-operativa\continuidad\2026-11-06\evaluacion-sesiones\ejecuciones')
runs=json.loads(sys.stdin.read())
out=[]
for run in runs:
    matched=[]
    for path in logs.glob('*.jsonl'):
        try:
            with path.open(encoding='utf-8') as f:
                p=json.loads(f.readline()).get('payload',{})
            source=p.get('source')
            spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
            if spawn.get('parent_thread_id')==parent and spawn.get('agent_path')==run['agent']:
                matched.append((path,p))
        except (OSError,ValueError): pass
    if len(matched)!=1:
        out.append({**run,'runtime_verified':False,'matches':len(matched)}); continue
    path,meta=matched[0]
    contexts=[]; usage=[]; actions=[]; completions=[]; finals=[]; results=[]; compaction_markers=[]; tool_output_chars=0
    with path.open(encoding='utf-8') as f:
        for line in f:
            item=json.loads(line); p=item.get('payload',{}); stamp=item.get('timestamp')
            if item.get('type')=='compacted' or p.get('type') in ('context_compacted','context_compaction'):
                compaction_markers.append({'timestamp':stamp,'type':item.get('type'),'event_type':p.get('type')})
            if item.get('type')=='turn_context':
                contexts.append({'timestamp':stamp,'model':p.get('model'),'effort':p.get('effort')})
            elif item.get('type')=='event_msg':
                if p.get('type')=='token_count' and p.get('info'):
                    usage.append({'timestamp':stamp,**p['info']})
                elif p.get('type') in ('task_complete','turn_complete'):
                    completions.append(stamp)
            elif item.get('type')=='response_item':
                kind=p.get('type')
                if kind in ('function_call','custom_tool_call'):
                    arguments=p.get('arguments',p.get('input'))
                    if p.get('name')=='send_message':
                        try:
                            envelope=json.loads(arguments)
                            if str(envelope.get('message','')).startswith('gAAAA'):
                                envelope['message']='[Payload opaco omitido; no es evidencia textual evaluada.]'
                                arguments=json.dumps(envelope,ensure_ascii=False)
                        except (ValueError,TypeError): pass
                    actions.append({'timestamp':stamp,'type':kind,'name':p.get('name'),'call_id':p.get('call_id'),'arguments':arguments})
                elif kind in ('function_call_output','custom_tool_call_output'):
                    tool_output_chars+=len(str(p.get('output','')))
                    output=p.get('output')
                    if isinstance(output,str) and output.startswith('gAAAA'):
                        output='[Resultado opaco omitido; no se intentó descifrar.]'
                    results.append({'timestamp':stamp,'type':kind,'call_id':p.get('call_id'),'output':output})
                elif kind=='message' and p.get('role')=='assistant':
                    text='\n'.join(x.get('text','') for x in p.get('content',[]) if x.get('type') in ('output_text','text'))
                    if text: finals.append({'timestamp':stamp,'phase':p.get('phase'),'text':text})
    summary={**run,'runtime_verified':bool(contexts),'thread_id':meta.get('id'),'started_at':meta.get('timestamp'),'completed_at':completions[-1] if completions else None,'contexts':contexts,'first_usage':usage[0] if usage else None,'usage_series':usage,'last_usage':usage[-1] if usage else None,'tool_calls':len(actions),'tool_output_characters':tool_output_chars,'compaction_markers_observed':compaction_markers}
    # Store tool inputs and public assistant messages only. Never persist model reasoning.
    target=base/run['run_id']
    if target.parent!=base: raise ValueError('Invalid run ID')
    target.mkdir(parents=True,exist_ok=True)
    (target/'runtime.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (target/'trace-actions.json').write_text(json.dumps({'actions':actions,'assistant_messages':finals},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (target/'trace-results.json').write_text(json.dumps({'results':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    out.append({k:summary[k] for k in ('run_id','runtime_verified','thread_id','contexts','started_at','completed_at','tool_calls','tool_output_characters')})
print(json.dumps(out,ensure_ascii=False))

