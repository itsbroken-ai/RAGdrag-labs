"""Every launcher must honor the same Python-resolution contract.

`start-fullchain.sh` resolved `PYTHON_BIN`, then `.venv/bin/python`, then
`python3`. The other five launchers hardcoded a bare `python` or `python3`, which
fails on any machine where that interpreter is absent or lacks the target
dependencies. Five of six targets were unreachable from a clean checkout.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

LAUNCHERS = [
    ("start-agentic.sh", "rag_server_agentic.py"),
    ("start-fullchain.sh", "rag_server_fullchain.py"),
    ("start-guarded.sh", "rag_server_guarded.py"),
    ("start-ingestible.sh", "rag_server_ingestible.py"),
    ("start-monitored.sh", "rag_server_monitored.py"),
    ("start-open.sh", "rag_server_open.py"),
]


@pytest.mark.parametrize("launcher,target", LAUNCHERS)
def test_launcher_honors_python_override(tmp_path, launcher, target):
    fake_python = tmp_path / "python"
    fake_python.write_text("#!/bin/sh\nprintf '%s\\n' \"$1\"\n")
    fake_python.chmod(0o755)

    env = {**os.environ, "PYTHON_BIN": str(fake_python)}
    result = subprocess.run(
        [str(REPO_ROOT / launcher)],
        cwd=REPO_ROOT, env=env, check=True, capture_output=True, text=True,
    )
    assert result.stdout.splitlines()[0] == str(REPO_ROOT / "targets" / target)
