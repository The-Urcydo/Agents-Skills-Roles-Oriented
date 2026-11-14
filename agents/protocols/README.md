# Protocols

Rules between roles, including the steps of a cross-role interaction. Task procedures live in skills. Protocols are host-agnostic: the host repository supplies its work tracker, paths, and state names.

| Protocol | Rule |
|---|---|
| [Definition of done](definition-of-done.md) | What evidence makes work finished. |
| [Escalation](escalation.md) | When to ask the human, and how to ask. |
| [Handoff](handoff.md) | What a fresh session needs to continue. |
| [Parallel work](parallel-work.md) | How several agents avoid overwriting each other. |
| [Review](review.md) | Independence, findings, and verdicts. |

Protocols are not skills. A skill is a procedure loaded when a task matches; a protocol is a rule that applies whenever the role is active. Routing that changes an item's owner or status belongs in a role charter or a protocol, never in a skill.

A protocol stays host-agnostic: the host supplies its tracker, paths, and state names. Do not add a repository-specific tool command here; put it in the host's docs or a skill.
