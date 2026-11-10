#!/bin/sh
# Plantilla instalada con una versión fija; usar desde la terminal SSH del VPS.
set -eu
umask 077
exec /usr/bin/env -i HOME=/home/onia-codex-worker USER=onia-codex-worker \
  LOGNAME=onia-codex-worker PATH=/usr/bin:/bin \
  /usr/bin/python3 -I '@RELEASE@/configurar-retorno-boss.py'
