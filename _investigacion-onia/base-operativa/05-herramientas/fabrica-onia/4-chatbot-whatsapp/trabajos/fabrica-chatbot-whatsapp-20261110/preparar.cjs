'use strict';
// Sólo genera un archivo local. No importa workflows ni abre conexiones.
const fs = require('node:fs');
const path = require('node:path');
const leer = name => fs.readFileSync(path.join(__dirname, name), 'utf8');
function construir() {
  const motor = leer('motor.cjs').replace(/module\.exports = \{crearMotor, normalizarMeta, ejecutarEscenario\};\s*$/, '');
  const fixture = JSON.parse(leer('fixtures.json'));
  const catalogo = JSON.parse(leer('mensajes.json'));
  return {
    name: 'ONIA WhatsApp — ENSAYO LOCAL — NO IMPORTAR', active: false,
    nodes: [
      {id: 'manual', name: 'Manual', type: 'n8n-nodes-base.manualTrigger', typeVersion: 1,
        position: [0, 0], parameters: {}},
      {id: 'fixture', name: 'Fixture FICTICIO', type: 'n8n-nodes-base.code', typeVersion: 2,
        position: [260, 0], parameters: {mode: 'runOnceForAllItems', language: 'javaScript',
          jsCode: 'return [{ json: ' + JSON.stringify({escenario: fixture, catalogo}) + ' }];'}},
      {id: 'motor', name: 'Simular sin efectos', type: 'n8n-nodes-base.code', typeVersion: 2,
        position: [520, 0], parameters: {mode: 'runOnceForAllItems', language: 'javaScript',
          jsCode: motor + '\nconst entrada = $input.first().json;\nreturn [{json: ejecutarEscenario(entrada.escenario, entrada.catalogo)}];\n'}}
    ],
    connections: {
      Manual: {main: [[{node: 'Fixture FICTICIO', type: 'main', index: 0}]]},
      'Fixture FICTICIO': {main: [[{node: 'Simular sin efectos', type: 'main', index: 0}]]}
    },
    settings: {executionOrder: 'v1', saveDataErrorExecution: 'none', saveDataSuccessExecution: 'none',
      saveManualExecutions: false},
    pinData: {}
  };
}
if (require.main === module) {
  fs.writeFileSync(path.join(__dirname, 'workflow-n8n.json'), JSON.stringify(construir(), null, 2) + '\n');
  console.log('workflow-n8n.json escrito localmente; active=false; cero importaciones');
}
module.exports = {construir};
