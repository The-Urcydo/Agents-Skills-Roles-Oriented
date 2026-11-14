# Agents

The harness around the skill library.

| Folder | Purpose |
|---|---|
| `protocols/` | Rules between roles: handoff, review, escalation, definition of done, and parallel work |
| `adapters/` | Generated tool-specific files (Claude Code, OpenCode) and their config |
| `evals/` | Optional golden tasks that exercise skill discovery and behavior |

Skills live in `../skills/`; role charters live in `../roles/`. This folder does not own either. The rules for changing this folder are in [AGENTS.md](AGENTS.md).

## Charter and method

A role charter holds routing, ownership, and stop rules: who acts, what it owns, when it stops. A skill holds the procedure for one task: read order, checks, templates, and commands that do not move a work item. A fact lives in one place. If both need a fact, the charter states the rule and the skill points to it.

A role that is mostly routing needs no skill. A role that produces an artifact and has a method of its own gets one. A skill that only restates its charter is not added. The full contract is in [the role format](../docs/reference/role-format.md).

## Status

Protocols are in place. Adapters and evals remain documented placeholders: the adapter generator and the eval harness are separate batches. Adapters are generated from the source and are never hand-edited.

Related: [roles](../roles/README.md), [skills](../skills/README.md), and [the skill format](../docs/reference/skill-format.md).
