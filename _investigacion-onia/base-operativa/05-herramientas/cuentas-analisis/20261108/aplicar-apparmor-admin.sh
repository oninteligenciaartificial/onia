#!/usr/bin/env bash
# Preparado para revisión. El coordinador NO lo ejecuta sin aprobación administrativa.
set -euo pipefail
test "${1:-}" = --aprobado-por-sergio || { echo 'Falta aprobación explícita de Sergio.' >&2; exit 2; }
test "$(id -u)" -eq 0 || { echo 'Requiere consola administrativa UID0; no eleva privilegios.' >&2; exit 2; }
directorio=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
origen="$directorio/onia-chromium-1252.apparmor"
destino=/etc/apparmor.d/onia-chromium-1252
ejecutable=/home/onia-codex-worker/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome
test ! -e "$destino" && test ! -L "$destino" || { echo 'Destino preexistente: preservar y conciliar.' >&2; exit 2; }
printf '%s  %s\n' 272c545f4ea37f124187a8674cf6d5bcb58bf4b23466499c76958b6184ec87f2 "$origen" | sha256sum --check --status
printf '%s  %s\n' e44893f0eb826ba2e9c0e44e182f910e8d8473ce00b9eb7ae7a652512f02cd78 "$ejecutable" | sha256sum --check --status
apparmor_parser --skip-kernel-load --skip-cache -I /etc/apparmor.d "$origen"
install -o root -g root -m 0644 -- "$origen" "$destino"
apparmor_parser --skip-kernel-load --skip-cache "$destino"
apparmor_parser --add --skip-cache "$destino"
printf '%s\n' 'Perfil específico cargado. No se inició navegador. Continuar con pruebas separadas.'
