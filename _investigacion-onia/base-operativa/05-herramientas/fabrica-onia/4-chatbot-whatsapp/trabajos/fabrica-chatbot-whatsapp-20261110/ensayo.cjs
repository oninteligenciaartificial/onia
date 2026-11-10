'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

// Ejecuta únicamente los dos Code del artefacto en un contexto local sin require,
// process, fetch, red, disco, credenciales ni variables de entorno del host.
function ejecutarWorkflow(workflow) {
  if (workflow.active !== false || workflow.nodes.length !== 3) throw Error('ARTEFACTO_INVALIDO');
  let items = [];
  for (const id of ['fixture', 'motor']) {
    const nodo = workflow.nodes.find(n => n.id === id);
    if (nodo?.type !== 'n8n-nodes-base.code') throw Error('NODO_INVALIDO');
    const contexto = vm.createContext({$input: {first: () => items[0]}});
    items = new vm.Script('(function(){\n' + nodo.parameters.jsCode + '\n})()')
      .runInContext(contexto, {timeout: 1000});
  }
  return JSON.parse(JSON.stringify(items[0].json));
}
if (require.main === module) {
  const workflow = JSON.parse(fs.readFileSync(path.join(__dirname, 'workflow-n8n.json'), 'utf8'));
  process.stdout.write(JSON.stringify(ejecutarWorkflow(workflow), null, 2) + '\n');
}
module.exports = {ejecutarWorkflow};
