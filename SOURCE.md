# Source Sync

This repository is a Codex community port of
[`epoko77-ai/im-not-ai`](https://github.com/epoko77-ai/im-not-ai).

- Functional source version: `v2.3.0`
- Functional source tag object: `578c53d7585ceb7063bc2344bd409cf228a44514`
- Functional source commit: `82137e858763dadb99561f194c5c00465735017b`
- Fork lineage: `Squirbie/im-not-ai-codex`
- Distribution repository: `devyouth94/im-not-ai-codex`
- Codex plugin version: `2.3.0`
- Sync date: `2026-07-24`

## Porting policy

Taxonomy, rules, deterministic scripts, gates, route policy, role behavior and
upstream README history are ported source-first. Changes are limited to the
Codex adapter boundary:

- plugin-relative paths and packaging
- Codex Desktop and CLI marketplace installation
- real Codex subagents for standard and heavy runtime roles
- runtime model selection left to the user's Codex settings
- explicit role input/output boundaries
- current distribution metadata and issue routing

The port does not claim byte-identical model output, token usage or execution
time across Claude Code and Codex.

## File mapping

- upstream `.claude/skills/humanize-korean/SKILL.md`
  → `plugins/im-not-ai/skills/humanize-korean/SKILL.md`
- upstream `.claude/skills/humanize-korean/references/`
  → `plugins/im-not-ai/skills/humanize-korean/references/`
- upstream runtime role prompts
  → `plugins/im-not-ai/skills/humanize-korean/references/agents/`
- upstream `scripts/`
  → `plugins/im-not-ai/scripts/`
- upstream offline tests and golden fixtures
  → `plugins/im-not-ai/tests/`
- upstream `README.md`
  → `README.md`, with only Codex-specific installation, runtime, path and
  distribution differences adapted

## Initial v2.3 Codex scope

Included:

- light, standard and heavy execution paths
- `humanize-diagnostician`, `humanize-monolith`, `humanize-finalizer`
- deterministic metrics, routing, chunking, reassembly and structural gates
- Codex plugin manifest and repository marketplace
- offline tests and Codex contract/security tests

Excluded:

- Claude Code commands, agents and install scripts
- retired, release-development and research roles
- web UI and web-service design artifacts
- automatic upstream synchronization

Future upstream versions are reviewed and ported manually.
