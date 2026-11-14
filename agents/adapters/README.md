# Adapters

Planned generated tool-specific files that point at the canonical skills and roles.

- Claude Code: `.claude/skills/<name>/` and `.claude/agents/<role>.md`, generated from `skills/` and `roles/`.
- OpenCode: the configured skills directory, generated from the same source.
- Other agents: add a target to `targets.json` and extend `tools/sync_adapters.py`.

The generator is not implemented yet. Until it lands, use `python3 tools/install.py` for skills. No adapter output should be hand-edited once the generator exists; the generator will record what it wrote and the checker will fail on drift.

The optional role fields `access: read-only` and `use_when` are tool-neutral hints. A future adapter may map `access` to a tool limit and `use_when` to the description that makes a callable role discoverable. Such a limit is coarser than the rule: it guards against accidents, not a determined session. Nothing enforces either field yet; the role's `never` list is the binding rule.
