# Handoff protocol

A session ends and a fresh one starts with no memory. The handoff file is the memory. The host repository supplies the tracker and the state names; this protocol defines the rules, not the format.

## What the handoff must answer

A fresh session must be able to answer five questions without the old conversation:

1. Where are we now?
2. What is already decided?
3. What has already failed?
4. What is the next action, and who does it?
5. What must not happen next?

The `write-handoff` skill gives the detailed format and examples.

## Reference state machine

This repository has no tracker tool. If the host has one, its states win. If it has none, use these names in the handoff so a fresh session can read the state the same way every time:

| From | Can move to |
|---|---|
| `draft` | `planned`, `blocked`, `canceled` |
| `planned` | `in-progress`, `blocked`, `draft`, `canceled` |
| `in-progress` | `in-review`, `blocked`, `planned`, `canceled` |
| `in-review` | `verified`, `in-progress`, `blocked`, `draft`, `canceled` |
| `verified` | `done`, `in-progress`, `canceled` |
| `blocked` | `draft`, `planned`, `in-progress`, `canceled` |
| `stale` | `draft`, `planned`, `in-progress`, `in-review`, `canceled` |
| `done` | final; archive it |
| `canceled` | final; archive it |

A stale handoff is untrusted: re-verify its claims before acting on it. A `blocked` item names what unblocks it; a `canceled` item names why.

## Rules

1. Whoever holds the item keeps the handoff current. Update it whenever you would hate to lose the context.
2. Change the state through the tracker's tool, not by editing the state field by hand.
3. Every status that means "review", "verified", or "done" needs evidence, not an assertion.
4. Review, verified, and done need an independent review: the agent that built the work never marks it verified or done.
5. A stale handoff is untrusted: re-verify its claims against the code and the branch before acting on them.
6. The handoff travels with the item. If the work moves to another branch or worktree, the handoff moves with it.

## Docs for the scribe

Before handoff, the builder writes one line in the handoff or pull request description:

- `Docs for the scribe: none, behavior unchanged.` when no behavior changed and no doc describes what was touched;
- `Docs for the scribe: <the docs to update, and the changelog line>` otherwise.

The reviewer checks the line against the diff. A `none` the diff supports lets the item skip the scribe and go to the orchestrator to close. A missing line, a listed doc, a changed behavior, or a `none` the diff contradicts keeps the scribe. The reviewer never rewrites the builder's line.

## Starting a session

1. Read the repository's agent rules, then find your item in the tracker.
2. Read its handoff. Respect the do-not list.
3. If the handoff is stale, re-verify before trusting it.
4. Do the next action. Update the handoff as you go; move the state when done.

Related: [definition of done](definition-of-done.md), [review](review.md), and the `write-handoff` skill.
