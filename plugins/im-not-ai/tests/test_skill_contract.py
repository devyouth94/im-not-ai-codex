"""Static contract checks for the source-first Codex v2.3 port."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = PLUGIN_ROOT / "skills" / "humanize-korean"
SKILL_PATH = SKILL_DIR / "SKILL.md"
ROLES_DIR = SKILL_DIR / "references" / "agents"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL_PATH.read_text(encoding="utf-8")
        cls.manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        cls.roles = {
            path.name: path.read_text(encoding="utf-8")
            for path in ROLES_DIR.glob("*.md")
        }

    def test_codex_routes_and_bundled_scripts(self) -> None:
        self.assertEqual(self.manifest["version"], "2.3.0")
        self.assertIn("humanize-korean v2.3", self.skill)
        self.assertIn("light는 오케스트레이터가 monolith 계약을 직접 수행", self.skill)
        self.assertIn("standard/heavy는 실제 Codex 서브에이전트를 사용", self.skill)
        self.assertIn("서브에이전트 위임을 사용할 수 없으면", self.skill)
        self.assertIn("병렬 호출", self.skill)
        self.assertIn("최대 4", self.skill)
        for script in (
            "prepare_monolith_input.py",
            "reassemble_chunks.py",
            "verify_gates.py",
        ):
            self.assertIn(f"../../scripts/{script}", self.skill)

    def test_only_runtime_role_contracts_are_bundled(self) -> None:
        self.assertEqual(
            set(self.roles),
            {
                "humanize-diagnostician.md",
                "humanize-finalizer.md",
                "humanize-monolith.md",
            },
        )

        expected = {
            "humanize-diagnostician.md": (
                "`input_path`",
                "`taxonomy_path`",
                "`output_path`",
            ),
            "humanize-monolith.md": (
                "`input_path`",
                "`quick_rules_path`",
                "`output_path`",
            ),
            "humanize-finalizer.md": (
                "`original_path`",
                "`rewritten_path`",
                "`diagnosis_path`",
                "`output_path`",
                "`report_path`",
            ),
        }
        for name, fields in expected.items():
            text = self.roles[name]
            for field in fields:
                self.assertIn(field, text)
            self.assertIn("shell, network, Git", text)

    def test_each_runtime_role_uses_a_fresh_subagent(self) -> None:
        self.assertIn("각 역할 호출(청크별 monolith 호출 포함)은 새 Codex", self.skill)
        self.assertIn("`followup_task` 등 후속\n  메시지로 다른 역할", self.skill)
        self.assertIn("하나의 역할만 수행한다", self.skill)

    def test_upstream_behavior_contract_is_preserved(self) -> None:
        diagnostician = self.roles["humanize-diagnostician.md"]
        monolith = self.roles["humanize-monolith.md"]
        finalizer = self.roles["humanize-finalizer.md"]

        self.assertIn("카운트 > 0인 지표는 이미 확정된 증거", diagnostician)
        self.assertIn("지배하는 순서로 3~6개", diagnostician)
        self.assertIn("D 카테고리(관용구 삭제) 먼저", monolith)
        self.assertIn("A → I → G → H → F → B → C·J → E 순서", monolith)
        self.assertIn("단계 3 부분 재실행 (최대 1회)", monolith)
        self.assertIn("over_polish_aborted: true", monolith)
        self.assertIn("의미 보존 검사 (메모리) — 15항", finalizer)
        self.assertIn("큰따옴표 인용 내부 불변", finalizer)
        self.assertIn("인과·조건·시간 순서 보존", finalizer)

        self.assertIn("monolith 자체검증 실패(6항 중 2+ 위반)", self.skill)
        self.assertIn("사용자가 검증·증적을 명시 요청", self.skill)
        self.assertIn("`--ignore-markup`", self.skill)
        self.assertIn("기존 run_id의 `final.md`를 새 입력으로 heavy P1부터", self.skill)
        self.assertIn("`final_prev.md`로 백업", self.skill)
        self.assertIn(
            "`genre_hint={genre}`, `strength={사용자 지정 또는 기본}`",
            self.skill,
        )
        self.assertIn("프로젝트 설정 등 다른 파일을 자동 파싱", self.skill)
        self.assertIn("light에서\n오케스트레이터가 이 계약을 직접 수행", monolith)
        self.assertIn("`output_mode=whole`", self.skill)
        self.assertIn("`output_mode=chunk`", self.skill)
        self.assertIn("`output_mode`: `whole | chunk`", monolith)
        self.assertIn("`output_mode=whole`이면 summary 블록을 정확히 1개", monolith)
        self.assertIn("`output_mode=chunk`이면 윤문한 청크 본문만", monolith)

    def test_claude_and_retired_workflow_tokens_are_absent(self) -> None:
        text = self.skill + "\n" + "\n".join(self.roles.values())
        for forbidden in (
            "model: opus",
            "${CLAUDE_SKILL_DIR}",
            ".claude/agents",
            "TeamCreate",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
