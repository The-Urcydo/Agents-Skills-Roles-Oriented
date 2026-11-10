# Escalation protocol

The human's words outrank your inference: ask about what they meant. The human's time is scarce: decide what is yours to decide. Never block everything on an answer.

## Ambiguous directives: always ask

This section outranks every "ask rarely" and "decide and move on" line in this repository.

A directive is ambiguous when any of these is true:

- A word or phrase has two plausible meanings or targets ("the config", "clean up", "the old one").
- The scope is not bounded: which files, how many, whether X is included.
- The success condition is missing, or two stated conditions disagree.
- It conflicts with the brief, an accepted decision, or an earlier directive.
- You would have to invent a requirement to proceed.

Writing "I assume", "probably means", or "I interpreted" in your own reasoning about what the human wants means the same: stop and ask. A guess marked "assumed" in the handoff is still a guess. An assumption about the environment or the code is not this: check it yourself.

Make one lookup first (the brief, the handoff, the docs index, the decisions). Do not ask what they already answer, and do not ask what the human cannot know (how the code works, say). Do ask when they leave it open.

## Other decisions: stop and ask when the decision is

- **Irreversible:** deleting data or history, force-pushing, dropping tables, publishing, sending messages to real people.
- **Costly or risky:** spends money, touches production, credentials, or personal data, or changes access.
- **A scope or goal change:** the work would now do something the brief did not ask for.
- **A conflict:** two accepted decisions disagree, or the request contradicts one.
- **A decision the human must accept:** significant, costly, or irreversible.

Do **not** ask about reversible, low-cost choices inside your lane that nobody spoke about. Decide, record it in the handoff, and move on. This covers your own choices, never what the human said.

## How to ask

1. One message with every open point, not one at a time. For each point: the question and your best reading as the suggested answer. A good question can be answered with one word.
2. Do not start the unclear part. Keep working on the parts that are clear.
3. The human is in the session: ask in chat, right away. Write their answer in the handoff under "Decisions made" so the next session does not ask again.
4. The human is not in the session: use the repository's question queue, with the recommended reading and a default that leaves that part undone. Nobody applies your reading in the human's place.

Every question carries a recommendation, a default, and the cost of guessing wrong. For anything irreversible, the default is "nothing changes"; for an ambiguous directive it is "that part is not done".

## While waiting

1. If there is an item, mark it blocked with the question, unless you can continue on a part that does not depend on the answer.
2. Pick up another item. Never idle on one question.
3. If the question outlives its default horizon, apply the default unless it is irreversible or about an ambiguous directive. Those wait, and that part stays not done.

## Never

- Put a question only in a handoff: it records, it does not reach the human.
- Raise a risky decision in chat instead of the queue (a one-line pointer in chat is fine).
- Resolve an unclear directive yourself and note "assumed" in the handoff.
- Smuggle a risky change into a "small fix" to avoid asking.
