# Acceso audiovisual OSS y piloto MCP · 8/11/2026

**Recomendación:** conservar `yt-dlp` para acceso público y captions, y `faster-whisper small/CPU/int8` existente para ASR cuando haya audio autorizado disponible. Reservar Playwright MCP para páginas, DOM accesible y capturas. No reinstalar ni incorporar ahora `youtube-transcript-api` o `whisper.cpp`: cubren alternativas, pero no resuelven por sí mismos los bloqueos observados. La comparación con licencias y fuentes primarias está en [ALTERNATIVAS](ALTERNATIVAS.md).

**Resultado del piloto: diagnóstico negativo reproducible.** El catálogo anuncia las cuatro herramientas autorizadas, pero la llamada real a `browser_navigate(https://example.com)` devuelve `MCP tool call requires approval, but approval policy is never`. `browser_close` devuelve el mismo error. No hay navegación, DOM ni captura acreditados; tampoco hay error de Chromium sandbox observado. La landing de Erik queda sin intentar por el bloqueo común de permisos. No existen `example.png` ni `erik.png` en esta entrega.

## Lo comprobado

Inventario del entorno actual, sin instalación ni cambios de configuración:

| Componente | Resultado |
|---|---|
| Node / Python del venv ASR | 20.20.2 / 3.12.3 |
| Playwright MCP existente | 0.0.84 en `~/operacion/browser-piloto-20261108` |
| playwright / playwright-core | 1.65.0-alpha-2026-10-30 |
| Chromium / headless shell | Binarios build 1252 presentes; ambos `ldd` rc=0, cero bibliotecas faltantes. Esto no prueba arranque. |
| ASR local | faster-whisper 1.2.1; CTranslate2 4.8.5; yt-dlp 2026.10.26; PyAV 18.1.0; `pip check` sin dependencias rotas |
| Alternativas no disponibles en el control consultado | `youtube-transcript-api` no instalado en ese venv; `whisper-cli` y `whisper.cpp` ausentes de PATH. No se inspeccionó todo el disco. |
| Control ASR nuevo | 2 s de silencio sintético, offline, modelo small ya presente, CPU int8, dos hilos y un worker: cero segmentos con VAD. Sólo carga/VAD; no exactitud de voz. |
| Hijo distinto | Mismo catálogo anunciado; sin navegación porque el padre no funcionó. IDs y límites en [EVIDENCIA](EVIDENCIA.md). |

El informe ASR anterior registra las pruebas reales de Pedro, Cormac y Justin y bloqueos de YouTube; se reutiliza como **evidencia documental anterior**, sin presentarla como inferencia nueva de esta sesión: [ejecución ASR](../../../03-referentes/asr/ejecucion-2026-11-08.md) y [Ali/Jeff](../../../03-referentes/asr/ali-jeff-intentos-2026-11-08.md). Acceder a captions/medios, transcribir voz y analizar imagen/sonido son comprobaciones distintas. ASR no certifica música, prosodia, edición, ritmo ni sincronía audiovisual.

## Reproducción del inventario y control local

Estos comandos usan instalaciones existentes; no instalar ni descargar pesos:

```bash
cat ~/operacion/browser-piloto-20261108/REPORTE.md
cat ~/operacion/browser-piloto-20261108/package.json
node --version
~/asr/venv/bin/python -m pip --disable-pip-version-check --no-cache-dir check
~/asr/venv/bin/python - <<'PY'
from importlib.metadata import version, PackageNotFoundError
for name in ('faster-whisper', 'yt-dlp', 'av', 'ctranslate2', 'youtube-transcript-api'):
    try: print(name, version(name))
    except PackageNotFoundError: print(name, 'no instalado en este venv')
PY
ldd ~/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome
```

Control offline repetible, sin archivo de audio ni salida de medios:

```bash
~/asr/venv/bin/python - <<'PY'
import os
from pathlib import Path
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['OMP_NUM_THREADS'] = '2'
os.environ['OPENBLAS_NUM_THREADS'] = '2'
import numpy as np
from faster_whisper import WhisperModel
paths = sorted(Path('/home/onia-codex-worker/asr/modelos/models--Systran--faster-whisper-small/snapshots').glob('*'))
assert len(paths) == 1, 'Se necesita exactamente un snapshot local; no descargar.'
model = WhisperModel(str(paths[0]), device='cpu', compute_type='int8',
                     cpu_threads=2, num_workers=1, local_files_only=True)
segments, info = model.transcribe(np.zeros(32000, dtype=np.float32),
                                 language='es', beam_size=5, vad_filter=True)
print([s.text for s in segments], info.duration, info.duration_after_vad)
PY
```

Esperado en el entorno inventariado: `[] 2.0 0.0`. No comparar 1,346 s y 620456 KiB observados con benchmarks de habla: incluyen carga/VAD sobre silencio y no ejercitan reconocimiento del habla. ONNX Runtime avisó que no pudo persistir un identificador de telemetría y usó memoria; el proceso terminó con rc=0. No se cambió su configuración para ocultar el aviso.

## Inyección explícita y reproducción MCP

El wrapper indicado por el briefing se localizó **sólo en el checkout coordinador**:

`~/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/codex-con-playwright.py`

Fue leído sin ejecutarlo ni modificarlo. No está en el HEAD inicial `c21792a8bd557d50188d55edfb8a3d3e5603c203` de este worktree; su versión publicada debe conciliarla el coordinador. Hash y configuración leída en [EVIDENCIA](EVIDENCIA.md). El wrapper agrega pares `-c mcp_servers.playwright.CLAVE=VALOR` al Codex real, conserva los argumentos del harness y usa Node local, transporte stdio sin puerto, `--headless --isolated --sandbox` y el Chromium existente. Limita `enabled_tools` a las cuatro herramientas y declara `default_tools_approval_mode=approve`. Esta lectura documenta intención; no permite certificar los argumentos efectivos del proceso padre ni que esa aprobación haya sido aplicada.

No se lanzó otro `codex exec`. La sesión actual recibió `approval_policy=never` y sandbox de escritura acotada por el harness. El rechazo demuestra que el runtime aún exige aprobación para las llamadas probadas. La documentación oficial admite [política por herramienta MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) y [claves de configuración](https://learn.chatgpt.com/docs/config-file/config-reference); no demuestra que agregar una clave vaya a corregir esta sesión.

Secuencia nativa para el próximo intento del coordinador, conservando el sandbox, `--ignore-user-config`, los mismos binarios y el catálogo acotado:

1. Enumerar `ALL_TOOLS` filtrando nombres `mcp__playwright__`; deben aparecer sólo `browser_navigate`, `browser_snapshot`, `browser_take_screenshot`, `browser_close`.
2. Invocar `mcp__playwright__browser_navigate({"url":"https://example.com"})`. En este intento fue rechazado antes de obtener resultado de página. Si se repite el rechazo, detener el flujo y conservar el diagnóstico.
3. Sólo si navega, invocar `browser_snapshot({})`, confirmar URL/título/`Example Domain` y `browser_take_screenshot({"filename":"_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/capturas/example.png","scale":"css","type":"png"})`.
4. Navegar a `https://cursos.eriktaveras.com/c/hermes-basico/`; registrar URL/título, snapshot y captura con la misma ruta base y nombre `erik.png`. Si hay 403/429/captcha/auth, detener esa ruta. No formularios, compras, login ni importación de cookies.
5. Invocar `browser_close({})` aun si falla la navegación; registrar su respuesta. Después, y sólo después, el hijo puede probar `example.com` si el padre logró navegar. No compartir navegador concurrentemente.

## Salida concreta y pendientes

**Responsable siguiente: coordinador.** Conciliar la política efectiva de herramientas con el wrapper que ya declara `approve`, el catálogo recibido y `approval_policy=never`. Como candidato de corrección acotada para un próximo lanzamiento, revisar las cuatro claves `mcp_servers.playwright.tools.<herramienta>.approval_mode="approve"`; es una propuesta sin prueba, no un cambio realizado ni una garantía. No cambiar configuración global, ampliar herramientas o desactivar sandbox. Recuperar/versionar el wrapper exacto antes del nuevo intento y repetir la secuencia anterior; si luego falla Chromium, conservar ese error como una causa nueva. No repetir la condición actual sin cambio identificado.

Cuenta `onia.investigacion`, perfil persistente y autenticación siguen **PROPUESTA**. No se crearon cuentas, credenciales ni perfiles ni se probó disponibilidad de Gmail. No se consumió vidIQ ni API paga. No hace falta una cuenta para el control público solicitado.

La entrega en rama queda para revisión independiente de sólo lectura por otra sesión, que ejecutará el coordinador después de `cerrar`. El hijo investigador no sustituye ese revisor. No se acepta ni integra a `master` desde esta ejecutora. [PRUEBA.json](PRUEBA.json) conserva acciones, resultados, hashes y límites; no es el registro canónico de la tarea.
