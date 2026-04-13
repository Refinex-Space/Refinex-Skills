#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SKILLS=(
  "harness-fix"
  "harness-feat"
  "harness-garden"
  "harness-verify"
)

passed=0
failed=0
skipped=0

echo "=== Harness live trigger tests ==="

for skill in "${SKILLS[@]}"; do
  prompt_file="${SCRIPT_DIR}/prompts/${skill}.txt"
  echo
  echo "Testing: ${skill}"

  if bash "${SCRIPT_DIR}/run-trigger-test.sh" "${skill}" "${prompt_file}"; then
    passed=$((passed + 1))
  else
    status=$?
    if [[ "${status}" -eq 2 ]]; then
      skipped=$((skipped + 1))
    else
      failed=$((failed + 1))
    fi
  fi
done

echo
echo "Passed: ${passed}"
echo "Failed: ${failed}"
echo "Skipped: ${skipped}"

if [[ "${failed}" -gt 0 ]]; then
  exit 1
fi
