# Review protocol

Independent review is the main quality gate in a repo with no human in the loop for every change.

## Independence

- The agent doing the review is never the agent that built the item. With a single model playing both parts, use a fresh session with no memory of the build, and read the brief before the author's summary.
- The review does not fix findings. Fixing makes the review a second builder and removes the second pair of eyes.

## Route before the verdict

Read the brief or issue's security-review decision before you start.

- If it says `required` and no security review exists, hand the item to the security role before any verdict. If the role is not installed, or the item has no place for a separate review, stop and ask the human; do not skip it.
- If a security review exists, read it before you start. A blocker or major finding means `changes requested`, unless the human accepted the risk. An "escalate to human" verdict is a question for the human, not yours.
- If it says `not needed`, or no decision is recorded, carry on. Do not send the item to security to be safe.

## Rules

- The review starts from the brief, not the author's summary.
- The reviewer runs the checks. Pasted output is not evidence.
- Every acceptance criterion gets evidence: a command, an output, a file, or a link.
- Check the rules: decisions respected, ownership respected, generated files in sync, the security-review decision resolved, and the builder's docs-for-the-scribe line holds against the diff. Docs and the changelog are the scribe's job after the review.
- Rank findings and state what, where, why, and the fix. Do not fix them.
- The verdict names the exact commit or diff and matches the findings.

The `review-work` skill is the procedure. The severity scale is in [the review-work reference](../../skills/review-work/references/severity.md).

## Verdicts

- **approve:** all criteria met, no blocker or major finding.
- **changes requested:** fix the findings and re-review.
- **reject:** the approach is wrong; re-plan or drop it.

A second review is needed after changes requested if any blocker was found.

## Route after the verdict

- **approve:** if the builder wrote `Docs for the scribe: none, behavior unchanged.` and the diff agrees, hand the item to the orchestrator to close. Otherwise hand it to the scribe. Never rewrite the builder's line.
- **changes requested:** hand the item back to the builder with the findings.
- **reject:** send it back to planning or drop it, with the reason.

Related: [definition of done](definition-of-done.md), [escalation](escalation.md), and the `review-work` skill.
