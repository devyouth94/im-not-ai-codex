"""Security regressions for plugin-local scripts and run artifacts."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PREPARE_SCRIPT = PLUGIN_ROOT / "scripts" / "prepare_monolith_input.py"
REASSEMBLE_SCRIPT = PLUGIN_ROOT / "scripts" / "reassemble_chunks.py"


class RunDirectorySecurityTests(unittest.TestCase):
    def _run(
        self, script: Path, *args: str, cwd: Path
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_prepare_rejects_run_dir_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root / "outside"
            result = self._run(
                PREPARE_SCRIPT,
                "--run-dir",
                str(outside),
                "--text",
                "오늘 비가 왔다.",
                cwd=root,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("_workspace", result.stderr + result.stdout)
            self.assertFalse((outside / "01_input.txt").exists())

    def test_prepare_rejects_outside_chunk_dir_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root / "outside"
            outside.mkdir()
            (outside / "01_input.txt").write_text("테스트 입력", encoding="utf-8")
            sentinel = outside / "02_chunk_01_rewritten.txt"
            sentinel.write_text("보존할 내용", encoding="utf-8")

            result = self._run(
                PREPARE_SCRIPT,
                "--chunk",
                "--run-dir",
                str(outside),
                cwd=root,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "보존할 내용")

    def test_prepare_rejects_diagnosis_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "_workspace" / "test-001"
            run_dir.mkdir(parents=True)
            (run_dir / "01_input.txt").write_text("테스트 입력", encoding="utf-8")
            diagnosis = root / "diagnosis.md"
            diagnosis.write_text("외부 진단", encoding="utf-8")

            result = self._run(
                PREPARE_SCRIPT,
                "--run-dir",
                str(run_dir),
                "--diagnosis",
                str(diagnosis),
                cwd=root,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((run_dir / "01_input_with_metrics.txt").exists())

    def test_prepare_writes_only_inside_workspace_and_ignores_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run_dir = root / "_workspace" / "test-001"
            result = self._run(
                PREPARE_SCRIPT,
                "--run-dir",
                str(run_dir),
                "--text",
                "오늘 비가 왔다.",
                cwd=root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((run_dir / "01_input.txt").exists())
            self.assertEqual(
                (run_dir / ".gitignore").read_text(encoding="utf-8"),
                "*\n!.gitignore\n",
            )

    def test_reassemble_rejects_run_dir_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root / "outside"
            outside.mkdir()
            result = self._run(
                REASSEMBLE_SCRIPT,
                "--run-dir",
                str(outside),
                cwd=root,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("_workspace", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
