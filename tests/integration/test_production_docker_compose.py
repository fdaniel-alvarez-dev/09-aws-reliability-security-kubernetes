from __future__ import annotations

import subprocess
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(cmd: list[str], *, timeout_s: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
    )


class TestProductionDockerCompose(unittest.TestCase):
    def test_end_to_end_drill(self) -> None:
        try:
            _run(["docker", "compose", "up", "-d", "--build"], timeout_s=600)

            deadline = time.time() + 90
            while True:
                try:
                    _run(
                        [
                            "docker",
                            "exec",
                            "-i",
                            _run(["docker", "compose", "ps", "-q", "postgres-primary"]).stdout.strip(),
                            "psql",
                            "-U",
                            "app",
                            "-d",
                            "appdb",
                            "-c",
                            "select 1;",
                        ],
                        timeout_s=30,
                    )
                    break
                except Exception:
                    if time.time() > deadline:
                        raise
                    time.sleep(2)

            _run(["make", "check"], timeout_s=120)
            _run(["make", "backup"], timeout_s=120)
            _run(["make", "restore"], timeout_s=180)
        finally:
            subprocess.run(["docker", "compose", "down", "-v"], cwd=str(REPO_ROOT), check=False)

