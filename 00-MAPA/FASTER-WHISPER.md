# Faster-Whisper y herramientas de edición/ASR · estado al 8 nov 2026

## Veredicto corto
**Existió y funcionó** (5 nov 2026), pero **hoy no está disponible para el usuario `onia-codex-worker`**:
- `python3 -c "import faster_whisper"` → `ModuleNotFoundError`; `ctranslate2` tampoco; `pip` no existe para este usuario.
- La instalación real está en un **contenedor Docker propio** `onia-asr-pilot-20261105` (Python 3.11-slim, faster-whisper 1.2.1, CTranslate2 4.8.5, modelo Systran faster-whisper-small, CPU int8) con datos en `/opt/onia-asr-pilot-20261105/` (root, permiso denegado). Este usuario no tiene acceso al socket Docker (`permission denied`), así que no pude ver si el contenedor sigue existiendo; según el repo quedó **detenido**.
- Los 16 ASR de referentes (Hormozi, Heras, Toto, Gonzalo, Pedro, Alex, Voltra…) se hicieron con faster-whisper 1.2.1 small **en local** (rutas `C:/dev/proyectos/...` del PC Windows); sus TXT/JSON quedaron en `operacion/` (gitignored) → no están en el repo ni en el VPS.
- No corrí smoke test: no hay módulo instalado para este usuario y sin root/Docker no es "trivialmente barato".

## Qué hay en el VPS (usuario worker)
- `ffmpeg` (/usr/bin/ffmpeg) y `yt-dlp` (/usr/local/bin/yt-dlp): **sí instalados**.
- 4 CPU, 15 GB RAM (9 GB disponibles al revisar).
- `/opt/onia-referentes-media/` (root): medios de referentes, p. ej. reel Cormac; probablemente parte de los MP4 "perdidos" (no verificable sin permisos).
- `/opt/onia-conette-pilot-20261105/` (root): piloto CoNeTTE (captioning de audio).

## Qué demostró (repo)
Fuente: [`vps-faster-whisper.md`](../_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audio-tecnico/vps-faster-whisper.md), [`audio-tecnico/ESTADO.md`](../_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audio-tecnico/ESTADO.md), [`audiovisual/guiones-faltantes.md`](../_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audiovisual/guiones-faltantes.md).
- **Sin VAD falla:** con silencio digital inventó "You". Configuración raw rechazada.
- **Con VAD (Silero, beam 5): funciona.** Silencio y tono → vacío; voz española con pausas y atenuada al 25% → frase exacta; jfk.flac → frase conocida; reel Cormac 37,8 s → similitud 0,9935 con otro ASR.
- Recursos: 1–2 CPU, 3 GiB, ~25 s para un reel de 38 s.
- Scripts en el repo: `audio-tecnico/vps-asr-pilot.py`, `vps-asr-vad.py`, `vps-supervisor.py`, `vps-preparar-pausas.py`; dependencias en `vps-dependencias-asr-instrumental.txt`.

## Para volver a usarlo (no hecho)
Opción A: arrancar el contenedor (`docker start onia-asr-pilot-20261105`) con un usuario con permiso Docker/root, y correr `vps-asr-vad.py` con VAD siempre activo.
Opción B: crear un venv de usuario (`python3 -m venv`, existe `/usr/lib/python3.12/venv`) e instalar `faster-whisper==1.2.1` (descarga ~500 MB con el modelo small). Requiere el sí de Sergio por uso de disco/red.
Siempre: `vad_filter=True`; nunca sin VAD.

## Edición de video
No hay herramienta de edición automática instalada ni documentada como funcionando en el VPS más allá de ffmpeg. El render local probado está en el commit `f39466f` ("prueba de render local", 4 nov), en el PC Windows.
