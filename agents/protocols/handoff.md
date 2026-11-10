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

## Rules

1. Whoever holds the item keeps the handoff current. Update it whenever you would hate to lose the context.
2. Change the state through the tracker's tool, not by editing the state field by hand.
3. Every status that means "review", "verified", or "done" needs evidence, not an assertion.
4. A stale handoff is untrusted: re-verify its claims against the code and the branch before acting on them.
5. The handoff travels with the item. If the work moves to another branch or worktree, the handoff moves with it.

## Starting a session

1. Read `AGENTS.md`, then find your item in the tracker.
2. Read its handoff. Respect the do-not list.
3. If the handoff is stale, re-verify before trusting it.
4. Do the next action. Update the handoff as you go; move the state when done.

Related: [definition of done](definition-of-done.md), [review](review.md), and the `write-handoff` skill.
