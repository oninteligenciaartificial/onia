// Local file transformation only. Does not import/execute n8n or SQL.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = __dirname;
const source = JSON.parse(fs.readFileSync(path.join(root, 'sources/workflow.cloud.json'), 'utf8'));
assert.equal(source.name, 'TANDA-01 CLAIM reserva PostgreSQL BORRADOR');
assert.deepEqual(source.nodes.map(n => n.name), ['Inicio manual', 'Fixture sintetico', 'Normalizar', 'Reservar transaccional', 'Solo revision', 'Resultado incierto']);
const normalize = [
  'const r=$input.first().json;',
  "if(r.synthetic!==true||r.account!=='IG_TEST_SYMBOLIC'||typeof r.event_id!=='string'||!/^SYNTH_[A-Za-z0-9_-]{1,80}$/.test(r.event_id)||typeof r.conversation_id!=='string'||!/^SYNTH_[A-Za-z0-9_-]{1,80}$/.test(r.conversation_id)||typeof r.text!=='string'||!r.text.trim()||r.text.length>500)throw new Error('FIXTURE_INVALID');",
  '// Preserve the exact text for conflict detection; normalization belongs to classification.',
  'const payload={schema_version:1,conversation_id:r.conversation_id,text:r.text,synthetic:true};',
  "return [{json:{account:r.account,event_id:r.event_id,payload_json:JSON.stringify(payload),mode:'LOCAL_STUB',draft_only:true}}];"
].join('\n');
const review = [
  'const r=$input.first().json;',
  "if(typeof r.inbox_id!=='string'||!/^[1-9][0-9]*$/.test(r.inbox_id))throw new Error('RESERVA_NO_VERIFICADA');",
  "const key=$('Normalizar').first().json;",
  "return [{json:{status:'RESERVA_CONFIRMADA_REVISION',account:key.account,event_id:key.event_id,inbox_id:String(r.inbox_id),mode:'LOCAL_STUB',dry_run:true,auto_send:false,sent:false,stub_result:'NOT_DISPATCHED',outbox_state_verification:'PENDIENTE_RUNTIME'}}];"
].join('\n');
const uncertain = [
  "const key=$('Normalizar').first().json;",
  '// Never echo a database error, connection string or driver metadata.',
  "return [{json:{status:'INCIERTO_O_CONFLICTO',account:key.account,event_id:key.event_id,payload_json:key.payload_json,mode:'LOCAL_STUB',dry_run:true,auto_send:false,sent:false,retry_allowed:false,action:'Conservar este resultado sintetico; consultar inbox/outbox por clave y comparar payload_json; no repetir a ciegas'}}];"
].join('\n');
const patch = [
  {op:'test',path:'/active',value:false},
  {op:'test',path:'/nodes/3/name',value:'Reservar transaccional'},
  {op:'replace',path:'/name',value:'ONIA reserva LOCAL_STUB · BORRADOR INACTIVO'},
  {op:'replace',path:'/nodes/1/parameters/jsCode',value:"return [{json:{synthetic:true,account:'IG_TEST_SYMBOLIC',event_id:'SYNTH_TANDA01_001',conversation_id:'SYNTH_CHAT_1',text:'PLAN'}}];"},
  {op:'replace',path:'/nodes/2/parameters/jsCode',value:normalize},
  {op:'replace',path:'/nodes/3/parameters/query',value:'SELECT onia_automation.reserve($1::text,$2::text,$3::jsonb)::text AS inbox_id;'},
  {op:'remove',path:'/nodes/3/credentials'},
  {op:'replace',path:'/nodes/4/parameters/jsCode',value:review},
  {op:'replace',path:'/nodes/5/parameters/jsCode',value:uncertain}
];
const local = structuredClone(source);
for (const op of patch) {
  const parts=op.path.slice(1).split('/').map(s=>s.replace(/~1/g,'/').replace(/~0/g,'~'));
  const key=parts.pop();
  const parent=parts.reduce((obj,k)=>obj[k],local);
  if(op.op==='test')assert.deepEqual(parent[key],op.value);
  else if(op.op==='remove')delete parent[key];
  else parent[key]=op.value;
}
fs.writeFileSync(path.join(root,'workflow.reserva.local.json'),JSON.stringify(local,null,2)+'\n');
fs.writeFileSync(path.join(root,'workflow.local.patch.json'),JSON.stringify(patch,null,2)+'\n');
console.log('Prepared local inactive JSON and RFC 6902 patch. No runtime execution.');
