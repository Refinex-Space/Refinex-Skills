#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=== Harness test suite ==="
echo "Root: ${ROOT_DIR}"
echo

echo "[1/2] 运行静态与 fixture 集成测试"
python3 -m unittest discover -s "${ROOT_DIR}/tests" -p "test_*.py"
echo

echo "[2/2] 运行可选 live trigger 测试"
if [[ "${HARNESS_RUN_LIVE:-0}" == "1" ]]; then
  bash "${ROOT_DIR}/tests/live/run-all.sh"
else
  echo "SKIP: 未设置 HARNESS_RUN_LIVE=1，跳过 live Codex 测试"
fi
