# Adapters

Generated tool-specific files that point at the canonical skills and roles.

- Claude Code: `.claude/skills/<name>/` and `.claude/agents/<role>.md`, generated from `skills/` and `roles/`.
- OpenCode: the configured skills directory, generated from the same source.
- Other agents: add a target to `targets.json` and extend `tools/sync_adapters.py`.

No adapter output is hand-edited. The generator records what it wrote and the checker fails on drift.

Batch 4 adds `targets.json` and `tools/sync_adapters.py`.
