# Agents

The harness around the skill library.

| Folder | Purpose |
|---|---|
| `protocols/` | Rules between roles: handoff, review, escalation, definition of done |
| `adapters/` | Generated tool-specific files (Claude Code, OpenCode) and their config |
| `evals/` | Optional golden tasks that exercise skill discovery and behavior |

Skills live in `../skills/`; role charters live in `../roles/`. This folder does not own either. Adapters are generated from the source and are never hand-edited.

Batch 4 adds the protocols and the adapter generator. Until then, this folder is a documented placeholder so the intended shape is clear.
