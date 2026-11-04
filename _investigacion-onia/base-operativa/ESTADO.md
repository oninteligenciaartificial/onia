# Estado y entrada operativa

## Continuar

Este proyecto usa las [reglas comunes](reglas-comunes.md). Las tareas verificables se guardan en `operacion/tareas/` y se consultan desde esta carpeta:

```powershell
python scripts/trabajo.py listar
python scripts/trabajo.py retomar base-001
```

Cada registro conserva objetivo, estado, resultado, comprobación, evidencia y próximo paso. Retomar es una lectura local; no inicia un agente ni una tarea programada. La comprobación de hashes detecta cambios de los archivos, no certifica su calidad.

## Trabajo vigente

**Corrección vigente:** Sergio creó un entorno limpio llamado `onia` y pidió repositorio propio de esta carpeta. La tarea anterior en ONIA Platform fue detenida y no es el entorno del harness. Preparar el repo con la base vigente, excluyendo proyectos vecinos, y vincularlo a `onia`. En la última consulta la herramienta no devolvió entornos disponibles; la vinculación/publicación y la prueba en el entorno correcto están pendientes.

- `base-001`: habilitar reglas, skills y continuidad local. Consultar el registro para su estado y evidencia.
- `video-001`: comprobar un render técnico de HyperFrames sin servicios generativos pagados.
- `cloud-001`: preparar el repositorio propio y el entorno limpio `onia`; no continuar en ONIA Platform. Alcance y criterio de terminado en README.md de la raíz. Esta preparación no espera al acceso del VPS.
- `vps-001`: inspección parcial de sólo lectura completada en Hostinger; URL n8n recibida y pantalla Sign in accesible. Ver operacion/evidencias/vps-inspeccion-2026-11-03.md. Autenticación n8n/API e inventario completo pendientes. No instalar cargas adicionales en el VPS de la startup.

Estas tareas pertenecen al encargo actual. La oferta comercial necesita todavía el resultado demostrable y el público que Sergio elegirá; ese faltante no bloquea construir esta base.

## Ubicaciones

- Contexto personal: `privado/contexto.md`, cargar sólo cuando corresponda.
- Skills propias: `compartibles/skills/`; descubrimiento local mediante enlaces en `C:/dev/proyectos/.agents/skills/`.
- Referencias y selección: `auditoria-30-repos.md` y `catalogo-repos-2026-11-03.json`.
- Errores y correcciones: `registro-de-errores.md`; conservar evidencias por caso, sin convertir todo en regla universal.

La tarea histórica 01a1a3e6-50ac-7052-9243-cafe9e8a200c, host durable, confirmó detención y ningún proceso activo. Cinco tests y continuidad aprobados en aquella VM; Chromium no se instaló por restricción de dominio. Esto no valida el entorno `onia`. Consultar cloud-001 para el último resultado. No hay scheduler ni worker desplegado. Los chats por área quedan para después de comprobar el entorno, según Sergio.
