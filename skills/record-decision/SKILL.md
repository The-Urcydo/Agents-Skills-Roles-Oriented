---
name: record-decision
description: "Record a significant technical decision as an architecture decision record with context, considered options, outcome, and consequences. Use when a choice is hard to reverse, has real alternatives, or future agents will ask why."
license: MIT
compatibility: "Works with a docs/decisions/ folder or any numbered ADR convention."
metadata:
  category: repo
  invocation: both
---
# Record a decision

Use this when a choice has real alternatives and a future reader will need the reason. A small reversible choice inside your remit belongs in the pull request, not an ADR.

## Steps

1. Read the existing decisions first. Accepted decisions are binding. If the new choice conflicts, propose a superseding record instead of working around it.
2. Decide whether the choice meets the bar: hard to reverse, costly, security-relevant, affects several parts, or likely to be questioned later. If not, record it in the pull request and stop.
3. Allocate the next number with the repository's tool. Do not guess a number or create the file by hand when a tool exists.
4. Write:
   - **Context and problem statement:** the forces and the question.
   - **Decision drivers:** what matters and why.
   - **Considered options:** at least two, with the real trade-offs.
   - **Decision outcome:** the chosen option and the reason.
   - **Consequences:** what gets better, what gets worse, and what stays neutral.
   - **Confirmation:** how the decision will be checked.
5. Set the status. A significant, costly, or irreversible decision starts as `proposed`; only the human moves it to `accepted`. A small reversible decision inside your remit may start as `accepted`.
6. Link the affected docs and code. Put the one-sentence summary in the front matter.
7. Run the repository's check and confirm the file name, number, status, and date are valid.

## Verify

- The record has context, at least two options, an outcome, and consequences.
- The number is unique and the file name follows the repository's convention.
- The status matches who approved it.
- A reader six months from now can understand why without asking.
- The check passes.

## In Repo-Template

```bash
python3 tools/new_adr.py "Title"
```

ADRs live in `docs/decisions/`. The tool allocates the number. A significant ADR starts as `proposed`; the human accepts it.

## Stop and ask

- The decision is irreversible, costly, security-relevant, or reverses an accepted decision.
- Two accepted decisions conflict.
- The human has not approved a decision that needs their sign-off.
- The record would include a secret or a personal path.
