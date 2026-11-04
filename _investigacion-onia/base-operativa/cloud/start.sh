#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PWD/../operacion/cloud-002/browsers}"
npm test
