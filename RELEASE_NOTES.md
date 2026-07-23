# v2.3.0 — Codex light·standard·heavy 포트

> 2026-07-24 · [`epoko77-ai/im-not-ai` v2.3.0](https://github.com/epoko77-ai/im-not-ai/releases/tag/v2.3.0) 기능 기준

기능 기준 원본의 v2.3.0 흐름을 Codex Desktop·CLI용 community
adapter로 옮겼습니다. 분류학·규칙·결정적 스크립트·게이트는 원본을
따르고, 실행 경계만 Codex에 맞췄습니다.

## 기능 기준 원본 v2.3.0

- `verify_gates.py` 4축 구조 수렴 게이트: 목표 달성, C-8 대구 전멸,
  수치 주입, golden 검사
- taxonomy에서 자동 생성하는 `diagnosis-rules.md`: 원본 taxonomy 대비
  83% 작은 진단 인덱스
- 대조 코퍼스 실증 결과와 이에 따른 A-2·I-1·C-8/C-14·E-1 규칙 보정
- `quick-rules.md`·`diagnosis-rules.md` drift 검사

## Codex adapter

- `route_hint` 기반 light 1콜, standard 2콜, heavy 3+콜
- standard/heavy의 실제 Codex 서브에이전트 실행
- diagnostician·monolith·finalizer와 각 monolith 청크를 서로 다른 새
  서브에이전트로 격리
- 모델·추론 강도는 현재 Codex 설정을 상속
- heavy 전용 결정적 청킹·재조립과 finalize 의미 보존 검사
- Codex marketplace 패키징과 Desktop·CLI 설치 절차

## 검증

- 오프라인 테스트 196개 통과, 1개 skip
- Ubuntu·macOS·Windows × Python 3.11·3.12 CI 통과
- macOS Codex CLI에서 light·standard·heavy 실행
- Codex Desktop 설치본에서 light·standard·heavy 게이트 통과
- standard 2역할과 heavy 3역할의 독립 서브에이전트 실행 확인

## 설치

```bash
codex plugin marketplace add devyouth94/im-not-ai-codex
codex plugin add im-not-ai-codex@im-not-ai-codex-marketplace
```

상세 설치·업데이트·사용법은 [`README.md`](README.md), 원본 동기화 기준은
[`SOURCE.md`](SOURCE.md)를 참고하세요.
