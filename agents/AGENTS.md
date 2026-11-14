# agents/ rules

- `agents/` holds the protocols, adapters, and evals around the skill library. Skills live in `../skills/`; role charters live in `../roles/`.
- A protocol is a rule between roles; a skill is a procedure for a task. Routing that changes who owns an item or its status belongs in a role charter or a protocol, never in a skill.
- Changes under `agents/` change every agent's behavior. They need the human owner's approval before merging.
- Keep protocols host-agnostic: no repository-specific paths, tracker commands, or tool names. The host supplies its work tracker and state names.
- Adapters and evals are placeholders until their batches land. Once an adapter generator exists, its output is generated; never hand-edit it.
- Never put secrets or personal paths in anything under `agents/`.
