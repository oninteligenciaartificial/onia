#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
onia_repo_root="$(cd ../../.. && pwd -P)"
onia_discovery_root="${ONIA_SKILLS_DISCOVERY_ROOT:-}"
# Codex Cloud inicia el agente en /workspace y el checkout en /workspace/onia.
# Fuera de ese layout no se toca el directorio padre sin selección explícita.
if [[ -z "$onia_discovery_root" && "$(dirname "$onia_repo_root")" == "/workspace" ]]; then
    onia_discovery_root="/workspace"
fi
onia_bootstrap_args=()
if [[ -n "$onia_discovery_root" ]]; then
    onia_bootstrap_args+=(--discovery-root "$onia_discovery_root")
fi
python3 ../scripts/preparar-cloud.py --install "${onia_bootstrap_args[@]}"
python3 ../scripts/preparar-cloud.py --check "${onia_bootstrap_args[@]}"
npm --cache "${ONIA_NPM_CACHE:-/tmp/onia-npm}" ci --no-audit --no-fund
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PWD/../operacion/cloud-002/browsers}"
npx --no-install playwright install chromium
