#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 ../scripts/preparar-cloud.py --install
python3 ../scripts/preparar-cloud.py --check
npm --cache "${ONIA_NPM_CACHE:-/tmp/onia-npm}" ci --no-audit --no-fund
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PWD/../operacion/cloud-002/browsers}"
npx --no-install playwright install --only-shell chromium
