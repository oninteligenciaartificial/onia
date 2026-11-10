#!/bin/sh
# Plantilla: sustituir @RELEASE@ por el directorio absoluto del commit revisado.
set -eu
umask 077
exec /usr/bin/env -i \
  HOME=/home/onia-codex-worker USER=onia-codex-worker LOGNAME=onia-codex-worker \
  PATH=/home/onia-codex-worker/.local/bin:/usr/bin:/bin \
  SSH_ORIGINAL_COMMAND="${SSH_ORIGINAL_COMMAND-}" \
  /usr/bin/timeout 300 /usr/bin/python3 -I '@RELEASE@/harness_boss.py' serve \
  /home/onia-codex-worker/operacion/puente-boss/config.json
