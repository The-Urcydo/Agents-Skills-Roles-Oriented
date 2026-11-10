# Agents

The harness around the skill library.

| Folder | Purpose |
|---|---|
| `protocols/` | Rules between roles: handoff, review, escalation, definition of done, and parallel work |
| `adapters/` | Generated tool-specific files (Claude Code, OpenCode) and their config |
| `evals/` | Optional golden tasks that exercise skill discovery and behavior |

Skills live in `../skills/`; role charters live in `../roles/`. This folder does not own either.

Protocols are in place. Adapters and evals remain documented placeholders: the adapter generator and the eval harness are separate batches. Adapters are generated from the source and are never hand-edited.

Related: [roles](../roles/README.md), [skills](../skills/README.md), and [the skill format](../docs/reference/skill-format.md).
