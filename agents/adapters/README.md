# Adapters

Planned generated tool-specific files that point at the canonical skills and roles.

- Claude Code: `.claude/skills/<name>/` and `.claude/agents/<role>.md`, generated from `skills/` and `roles/`.
- OpenCode: the configured skills directory, generated from the same source.
- Other agents: add a target to `targets.json` and extend `tools/sync_adapters.py`.

The generator is not implemented yet. Until it lands, use `python3 tools/install.py` for skills. No adapter output should be hand-edited once the generator exists; the generator will record what it wrote and the checker will fail on drift.
