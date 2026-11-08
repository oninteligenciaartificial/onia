# Encargo harness-interrupcion-real-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Interrumpir y retomar el mismo juguete sin perder cambios ni duplicar commits

## Entregable

Checkpoint preservado, entrega autónoma única y revisión independiente

## Criterio de aceptación

1. Antes de la señal externa existen checkpoint.json staged y nota.txt untracked, cero commits desde la base y ningún push. 2. Tras interrupción externa del PID Codex identificado, se conservan exactamente bytes, índice y HEAD; no quedan hijos activos del intento antes de retomar. 3. Los eventos thread.started reales de los tres intentos ejecutores tienen el mismo session ID, y conservan worktree/Git privado/rama. 4. Al retomar se completan exactamente cuatro archivos: checkpoint.json, nota.txt, resultado.json y verificar.py; checkpoint/nota conservan sus bytes iniciales. Resultado exacto {"valores":[6,9,12],"total":27,"checkpoint_sha256":"ab0a32d8c67d70450bd6d29dbae11f10aef561917223f49e4b289ce79d28f483"}. Verificador stdlib sin escrituras, lee desde su carpeta, devuelve RETOMA_OK con rc0 y rechaza discrepancias. 5. La propia ejecutora crea y publica exactamente UN commit. Otra retoma posterior comprueba y sale sin nuevo commit/push ni cambios; HEAD, remoto y conteo siguen iguales. 6. Revisor real distinto, sólo lectura, coteja entrega y recibos de interrupción/retoma/idempotencia y emite bueno antes de aceptar.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio autorizó interrupción real de esta sesión de juguete y retoma por su mismo ID. Sólo ChatGPT incluido, Sol/low. Sin API, compras, instalaciones, sudo, producción, Docker, n8n, app-server, mensajes, otros servicios ni sesiones/subagentes.
- Ruta exclusiva: 05-herramientas/2026-11-08-harness/piloto-interrupcion. Leer reglas pertinentes; no editar tarea/briefing canónicos ni archivos fuera de esta ruta. Git privado e identidad técnica ya preparados.
- Flujo idempotente. Primero inspeccionar HEAD, estado y archivos; no sobrescribir archivos existentes ni descartar cambios. Si no existe señal /home/onia-codex-worker/operacion/controles/interrupcion-20261108/continuar.json: crear checkpoint.json con EXACTAMENTE estos bytes UTF-8 '{"etapa":"antes-interrupcion","valores":[6,9,12]}\n' y nota.txt con EXACTAMENTE 'Nota sin seguimiento: conservar estos bytes al retomar.\n'. Usar git add sólo para checkpoint.json; nota.txt queda untracked. No crear resultado/verificador, commit o push todavía.
- En el primer intento, después de crear y stagear checkpoint, ejecutar ÚNICAMENTE este lector en un comando de shell aparte. No encadenar creación de archivos, commit ni push después del bloque. El coordinador interrumpirá externamente tu proceso mientras espera:
python3 - <<'PYWAIT'
from pathlib import Path
import json,time
p=Path("/home/onia-codex-worker/operacion/controles/interrupcion-20261108/continuar.json")
limit=time.monotonic()+300
print("INTERRUPCION_ESPERANDO",flush=True)
while not p.exists():
    if time.monotonic()>limit: raise SystemExit("ESPERA_TIMEOUT")
    time.sleep(0.25)
assert json.loads(p.read_text())["continuar"] is True
print("LECTOR_TERMINADO",flush=True)
PYWAIT
No mates procesos vos. La espera es sólo lectura y termina al ver la señal; no tiene efectos posteriores.
- Si la señal ya existe al retomar: conservar bytes e índice del checkpoint y la nota; no re-crear ni añadir líneas. Completar resultado.json con el objeto de aceptación y verificar.py que use stdlib, compruebe ambos archivos conservados, SHA256 del checkpoint y el resultado completo, sin escribir. Probar un caso correcto y discrepante sin modificar archivos de entrega (por ejemplo mocks en memoria).
- Antes de publicar contar commits desde la base registrada por el harness (origin/master local del Git privado). Si no hay commit de entrega, git add de los cuatro paths explícitos, git commit -m "test: interrupcion y retoma idempotente del harness", git push origin HEAD:refs/heads/codex/ws-harness-interrupcion-real-20261108. Si ya hay un commit válido, NO crear otro: comprobar y sólo hacer push si aún faltara remoto. Prohibidos amend, rebase, force, --allow-empty y modificar configuración global.
- Cuando HEAD y remoto ya coinciden y la entrega está completa, limitarse a ejecutar verificar.py, git status, git rev-parse HEAD, git rev-list --count origin/master..HEAD y git ls-remote origin refs/heads/codex/ws-harness-interrupcion-real-20261108; informar RETOMA_IDEMPOTENTE_OK y salir. No hacer git add/commit/push en ese caso. El coordinador hará una segunda retoma deliberada antes del cierre para verificarlo.
- Informar hash y evidencia. Si falla un permiso o la evidencia de estado no coincide, terminar e informar sin bypass. El coordinador no publicará la entrega por vos; hará cierre, revisión e integración después.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Cambio acotado de código
- Comprobación del comportamiento solicitado

## Registro

Estado: [registro de trabajo](../tareas/harness-interrupcion-real-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.
