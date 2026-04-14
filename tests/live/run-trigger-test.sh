#!/usr/bin/env bash

set -euo pipefail

EXPECTED_SKILL="${1:?expected skill required}"
PROMPT_FILE="${2:?prompt file required}"
TARGET_DIR="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if ! command -v codex >/dev/null 2>&1; then
  echo "SKIP: codex 不可用"
  exit 2
fi

if [[ ! -f "${PROMPT_FILE}" ]]; then
  echo "SKIP: prompt 文件不存在: ${PROMPT_FILE}"
  exit 2
fi

mkdir -p "${HOME}/.agents/skills"
LINK_PATH="${HOME}/.agents/skills/refinex-skills-live"
CREATED_LINK=0

if [[ ! -e "${LINK_PATH}" ]]; then
  ln -s "${ROOT_DIR}/skills" "${LINK_PATH}"
  CREATED_LINK=1
fi

cleanup() {
  if [[ "${CREATED_LINK}" -eq 1 && -L "${LINK_PATH}" ]]; then
    rm -f "${LINK_PATH}"
  fi
  if [[ -n "${TEMP_WORK_DIR:-}" && -d "${TEMP_WORK_DIR}" ]]; then
    rm -rf "${TEMP_WORK_DIR}"
  fi
}

trap cleanup EXIT

WORK_DIR="${TARGET_DIR}"
TEMP_WORK_DIR=""
if [[ -n "${WORK_DIR}" ]]; then
  if [[ ! -d "${WORK_DIR}" ]]; then
    echo "SKIP: 工作目录不存在: ${WORK_DIR}"
    exit 2
  fi
else
  TEMP_WORK_DIR="$(mktemp -d)"
  WORK_DIR="${TEMP_WORK_DIR}"
fi

LAST_MESSAGE="$(mktemp)"
STDERR_LOG="$(mktemp)"

PROMPT="$(cat "${PROMPT_FILE}")"

if ! timeout "${HARNESS_LIVE_TIMEOUT:-90}" codex exec \
  --ephemeral \
  --skip-git-repo-check \
  --sandbox read-only \
  -C "${WORK_DIR}" \
  -o "${LAST_MESSAGE}" \
  "${PROMPT}" \
  >/dev/null 2>"${STDERR_LOG}"; then
  if grep -Eq "No access token|403 Forbidden|authentication required|stream disconnected" "${STDERR_LOG}"; then
    echo "SKIP: Codex 登录态或网络不可用"
    exit 2
  fi
  echo "FAIL: Codex 执行失败"
  cat "${STDERR_LOG}"
  exit 1
fi

if [[ ! -s "${LAST_MESSAGE}" ]]; then
  echo "SKIP: 未获得可分析的最终回复"
  exit 2
fi

if grep -q "${EXPECTED_SKILL}" "${LAST_MESSAGE}"; then
  echo "PASS: ${EXPECTED_SKILL} 已在回复中显式出现"
  exit 0
fi

echo "FAIL: 最终回复未显式提到 ${EXPECTED_SKILL}"
echo "--- Last message ---"
cat "${LAST_MESSAGE}"
exit 1
