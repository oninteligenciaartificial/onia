#!/usr/bin/env bash
set -euo pipefail
ASR_ROOT="${ASR_ROOT:-/home/onia-codex-worker/asr}"
exec "$ASR_ROOT/venv/bin/python" "$ASR_ROOT/transcribir.py" "$@"
