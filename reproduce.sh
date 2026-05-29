#!/usr/bin/env bash
# reproduce.sh — Single-command framework verification
#
# Verifies the sbt-framework Python package builds, dependencies resolve,
# and the full unit-test suite passes (131 tests for validators + prompt
# generator). Conforms to PUBLIC_MIRROR_STANDARD.md v1.0.0.
#
# Usage:
#   ./reproduce.sh                  # Full sync + test
#   ./reproduce.sh --check-only     # Verify dependencies; do not run tests
#   ./reproduce.sh --fast           # Run only fast tests (skip slow markers)
#
# Run log lands in output/logs/master_run.log

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

mkdir -p output/figures output/tables output/logs
LOG_FILE="output/logs/master_run.log"

echo "==================================================" | tee -a "$LOG_FILE"
echo "Pipeline run: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "Repo: $REPO_ROOT" | tee -a "$LOG_FILE"
echo "Git SHA: $(git rev-parse HEAD 2>/dev/null || echo 'not-a-repo')" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

# Parse flags
CHECK_ONLY=0
FAST=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --fast) FAST=1 ;;
    *) echo "Unknown flag: $arg"; exit 2 ;;
  esac
done

# 1. Dependency check / install
echo ">>> Checking dependencies..." | tee -a "$LOG_FILE"
if command -v uv >/dev/null 2>&1; then
  uv sync --extra dev 2>&1 | tee -a "$LOG_FILE"
else
  echo "ERROR: uv not found. Install via 'curl -LsSf https://astral.sh/uv/install.sh | sh'" | tee -a "$LOG_FILE"
  exit 1
fi

if [[ "$CHECK_ONLY" == "1" ]]; then
  echo ">>> Check-only mode; exiting before tests." | tee -a "$LOG_FILE"
  exit 0
fi

# 2. Test suite — validators + prompt generator
echo ">>> Block 1: Running unit tests" | tee -a "$LOG_FILE"
if [[ "$FAST" == "1" ]]; then
  uv run pytest -q -m "not slow" 2>&1 | tee -a "$LOG_FILE"
else
  uv run pytest -q 2>&1 | tee -a "$LOG_FILE"
fi

echo "==================================================" | tee -a "$LOG_FILE"
echo "Pipeline complete: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"
