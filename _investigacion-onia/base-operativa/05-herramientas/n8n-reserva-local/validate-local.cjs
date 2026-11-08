// Static validation only. Code strings are compiled, NEVER executed.
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=__dirname;
const read=n=>fs.readFileSync(path.join(root,n),'utf8');
const w=JSON.parse(read('workflow.reserva.local.json'));
const checks=[];
function test(name,fn){try{fn();checks.push({name,passed:true});}catch(e){checks.push({name,passed:false,detail:e.message});}}
const source=JSON.parse(read('sources/workflow.cloud.json'));
test('source_files_sha256_match_remote',()=>{
  for(const f of JSON.parse(read('sources/manifest.json')).files)
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,f.file))).digest('hex'),f.sha256);
});
test('json_patch_reproduces_workflow',()=>{
  const reconstructed=structuredClone(source);
  for(const op of JSON.parse(read('workflow.local.patch.json'))){
    const parts=op.path.slice(1).split('/').map(s=>s.replace(/~1/g,'/').replace(/~0/g,'~'));const key=parts.pop();
    const p=parts.reduce((v,k)=>v[k],reconstructed);
    if(op.op==='test')assert.deepEqual(p[key],op.value);
    else if(op.op==='remove')delete p[key];
    else {assert.equal(op.op,'replace');assert.ok(Object.hasOwn(p,key));p[key]=op.value;}
  }
  assert.deepEqual(reconstructed,w);
});
test('inactive_no_workflow_or_version_identity',()=>{
  assert.equal(w.active,false);for(const k of ['id','versionId','webhookId','shared'])assert.ok(!Object.hasOwn(w,k));
});
test('unique_logical_nodes_preserved',()=>{
  assert.equal(w.nodes.length,6);assert.deepEqual(w.nodes.map(n=>[n.id,n.name]),source.nodes.map(n=>[n.id,n.name]));
  assert.equal(new Set(w.nodes.map(n=>n.name)).size,w.nodes.length);
});
test('graph_all_nodes_reachable_no_dangling_edges',()=>{
  const names=new Set(w.nodes.map(n=>n.name));const seen=new Set();
  for(const [from,channels]of Object.entries(w.connections)){assert.ok(names.has(from));assert.deepEqual(Object.keys(channels),['main']);
    for(const branch of channels.main)for(const edge of branch){assert.ok(names.has(edge.node));assert.equal(edge.type,'main');assert.equal(edge.index,0);}}
  function visit(n){if(seen.has(n))return;seen.add(n);for(const b of w.connections[n]?.main??[])for(const e of b)visit(e.node);}
  visit('Inicio manual');assert.equal(seen.size,w.nodes.length);
});
test('node_allowlist_no_sender_http_webhook_scheduler',()=>{
  const allowed=new Set(['n8n-nodes-base.manualTrigger','n8n-nodes-base.code','n8n-nodes-base.postgres']);
  for(const n of w.nodes)assert.ok(allowed.has(n.type),n.type);
  assert.equal(w.nodes.filter(n=>n.type==='n8n-nodes-base.postgres').length,1);
});
test('no_credential_bindings_or_embedded_connection_material',()=>{
  const forbidden=new Set(['credentials','credentialId','password','passwd','secret','apiKey','accessToken','authorization','headers','host','port','database','username','connectionString']);
  function walk(v){if(!v||typeof v!=='object')return;for(const[k,x]of Object.entries(v)){assert.ok(!forbidden.has(k),k);walk(x);}}
  walk(w);assert.doesNotMatch(JSON.stringify(w),/https?:\/\/|postgres(?:ql)?:\/\/|BEGIN [A-Z ]*PRIVATE KEY|Bearer\s|REEMPLAZAR_CREDENCIAL/i);
});
test('code_syntax_compiles_no_network_process_or_dynamic_execution',()=>{
  for(const n of w.nodes.filter(n=>n.type==='n8n-nodes-base.code')){
    new vm.Script('(function(){\n'+n.parameters.jsCode+'\n})',{filename:n.name});
    assert.doesNotMatch(n.parameters.jsCode,/\b(fetch|require|import|process|eval|Function|XMLHttpRequest|axios)\b|\$env|\$http|\.httpRequest/);
    for(const m of n.parameters.jsCode.matchAll(/\$\('([^']+)'\)/g))assert.ok(w.nodes.some(x=>x.name===m[1]));
  }
});
test('parameterized_reserve_without_retry_or_claim',()=>{
  const n=w.nodes.find(n=>n.name==='Reservar transaccional');
  assert.equal(n.parameters.query,'SELECT onia_automation.reserve($1::text,$2::text,$3::jsonb)::text AS inbox_id;');
  assert.equal(n.parameters.options.queryReplacement,'={{ [$json.account, $json.event_id, $json.payload_json] }}');
  assert.equal(n.retryOnFail,false);assert.equal(n.onError,'continueErrorOutput');
  assert.equal(w.connections[n.name].main[0][0].node,'Solo revision');assert.equal(w.connections[n.name].main[1][0].node,'Resultado incierto');
});
test('payload_retains_exact_text_no_volatile_fields',()=>{
  const code=w.nodes.find(n=>n.name==='Normalizar').parameters.jsCode;
  assert.match(code,/text:r\.text,synthetic:true/);assert.doesNotMatch(code,/toUpperCase|Date|random|executionId/);
});
test('stub_terminal_has_no_dispatch_and_errors_preserve_key',()=>{
  const ok=w.nodes.find(n=>n.name==='Solo revision').parameters.jsCode;
  const error=w.nodes.find(n=>n.name==='Resultado incierto').parameters.jsCode;
  assert.match(ok,/stub_result:'NOT_DISPATCHED'/);assert.match(ok,/sent:false/);assert.match(error,/retry_allowed:false/);
  assert.match(error,/payload_json:key.payload_json/);
  for(const c of[ok,error]){assert.match(c,/account:key.account,event_id:key.event_id/);assert.match(c,/auto_send:false/);}
  assert.ok(!w.connections['Solo revision']);assert.ok(!w.connections['Resultado incierto']);
});
test('execution_data_and_pinned_data_disabled',()=>{
  assert.equal(w.settings.saveDataSuccessExecution,'none');assert.equal(w.settings.saveDataErrorExecution,'none');
  assert.equal(w.settings.saveManualExecutions,false);assert.equal(w.settings.saveExecutionProgress,false);assert.deepEqual(w.pinData,{});
});
test('historical_sql_report_not_runtime_proof',()=>{
  const r=JSON.parse(read('sources/pg-qa.cloud.json'));assert.equal(r.n8n_atomicity_proven,false);assert.equal(r.external_exactly_once_proven,false);
  assert.equal(r.source_sha256,crypto.createHash('sha256').update(read('sources/transactional-outbox.cloud.sql')).digest('hex'));
});
const report={checked_at_utc:new Date().toISOString(),node:process.version,scope:'STATIC_LOCAL_ONLY',checks,passed:checks.filter(c=>c.passed).length,total:checks.length,n8n_import_tested:false,n8n_runtime_tested:false,sql_executed:false,atomicity_proven:false,notes:['No Code node executed; syntax compilation only.','Credential check is structural plus recognizable-pattern scan, not a universal secret detector.']};
fs.writeFileSync(path.join(root,'validation-results.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if(report.passed!==report.total)process.exitCode=1;
