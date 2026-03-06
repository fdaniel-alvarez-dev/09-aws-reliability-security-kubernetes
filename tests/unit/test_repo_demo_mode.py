from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestRepoDemoMode(unittest.TestCase):
    def test_k8s_validation_runs(self) -> None:
        subprocess.run([sys.executable, "scripts/k8s_validate.py"], cwd=str(REPO_ROOT), check=True)

    def test_security_validation_runs(self) -> None:
        subprocess.run([sys.executable, "scripts/security_validate.py"], cwd=str(REPO_ROOT), check=True)

