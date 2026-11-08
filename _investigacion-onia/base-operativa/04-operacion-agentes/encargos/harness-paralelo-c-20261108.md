# Encargo harness-paralelo-c-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Probar juguete c en paralelo con publicación autónoma

## Entregable

Dos archivos sintéticos, verificación y commit/push propios

## Criterio de aceptación

1. Diff sólo agrega resultado.json y verificar.py en 05-herramientas/2026-11-08-harness/piloto-paralelo/c. 2. JSON exacto {"tarea": "c", "valores": [11, 13, 17], "suma": 41, "maximo": 17}. 3. verificar.py usa sólo stdlib, lee desde su carpeta, comprueba objeto completo (sin aceptar floats/bools como enteros), sale 0 con PARALELO_C_OK, rechaza discrepancias y no escribe archivos. 4. La propia ejecutora hace add/commit/push de su rama desde sandbox sin escalación; HEAD coincide con origin. 5. Evidencia host acredita tres ejecutoras reales con PID/SID distintos y solape, rechazo de cuarta y rutas solapadas sin crear esos procesos. 6. Revisor distinto coteja entrega, pruebas y evidencia, emite bueno antes de aceptar.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio autorizó este piloto y revisor distinto. Sólo cuota incluida ChatGPT: no API, compras, sudo, instalaciones, producción, Docker, n8n, app-server, mensajes ni otros servicios. No lanzar sesiones ni subagentes.
- Una tarea y ruta exclusivas: 05-herramientas/2026-11-08-harness/piloto-paralelo/c. No modificar registros, reglas, archivos de otros juguetes ni metadatos de otros repositorios. Crear exactamente los dos archivos pedidos.
- Antes de crear la entrega, después de leer reglas/contexto, esperá la señal del coordinador con este comando de sólo lectura (no escribas ni crees la señal). No hace falta explorar otras carpetas ni pedir permiso:
python3 - <<'PYGATE'
from pathlib import Path
import json,time
p=Path("/home/onia-codex-worker/operacion/controles/paralelo-20261108/liberar.json")
limit=time.monotonic()+300
print("PARALELO_BARRERA_LISTO",flush=True)
while not p.exists():
    if time.monotonic()>limit: raise SystemExit("BARRERA_TIMEOUT; informar y terminar sin publicar")
    time.sleep(0.25)
assert json.loads(p.read_text())["liberar"] is True
print("PARALELO_BARRERA_LIBERADA",flush=True)
PYGATE
Si hay timeout o falla de permisos, informar y terminar, sin bypass. La espera no es una carga intensiva ni un servicio.
- Después de la señal, crear/verificar el juguete, probar al menos un objeto discrepante en memoria sin modificar el JSON, luego git add de los dos paths explícitos, git commit -m "test: juguete paralelo c del harness" y git push origin HEAD:refs/heads/codex/ws-harness-paralelo-c-20261108. Nunca force. Comprobar git rev-parse HEAD y git ls-remote origin refs/heads/codex/ws-harness-paralelo-c-20261108.
- El Git privado y la identidad técnica ya están preparados. Publicá vos desde el sandbox. El coordinador hará cierre, revisión e integración; no tu commit/push. Informar hash y comprobación.

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

Estado: [registro de trabajo](../tareas/harness-paralelo-c-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.
