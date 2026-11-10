# Handoff protocol

A session ends and a fresh one starts with no memory. The handoff file is the memory. The host repository supplies the tracker and the state names; this protocol defines the content, not the states.

## What the next session needs

- **Current state:** one paragraph on where things stand now.
- **Decisions made:** choices that must not be re-litigated, with a pointer to the decision record.
- **Dead ends already tried:** what failed and why.
- **Next action:** one sentence naming the next owner and the first thing they do.
- **Evidence:** the commands run and their result, or a link to the run.
- **Do not:** files, assumptions, or approaches the next agent must avoid.

Keep it under about 60 lines. It is current state, not a diary; history lives in git.

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
