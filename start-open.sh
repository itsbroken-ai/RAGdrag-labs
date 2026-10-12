#!/bin/bash
# Start the open RAG target (no guardrails)
# Requires: Ollama running locally, and the lab dependencies installed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-}"

if [[ -z "$PYTHON_BIN" ]]; then
    if [[ -x "$SCRIPT_DIR/.venv/bin/python" ]]; then
        PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
    else
        PYTHON_BIN="python3"
    fi
fi

OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3:0.6b}" exec "$PYTHON_BIN" "$SCRIPT_DIR/targets/rag_server_open.py"
