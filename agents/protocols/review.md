# Review protocol

Independent review is the main quality gate in a repo with no human in the loop for every change.

## Independence

- The agent doing the review is never the agent that built the item. With a single model playing both parts, use a fresh session with no memory of the build, and read the brief before the author's summary.
- The review does not fix findings. Fixing makes the review a second builder and removes the second pair of eyes.

## Rules

- The review starts from the brief, not the author's summary.
- The reviewer runs the checks. Pasted output is not evidence.
- Every acceptance criterion gets evidence: a command, an output, a file, or a link.
- Check the rules: decisions respected, ownership respected, generated files in sync, docs updated.
- Rank findings and state what, where, why, and the fix. Do not fix them.
- The verdict names the exact commit or diff and matches the findings.

The `review-work` skill is the procedure. The severity scale is in [the review-work reference](../../skills/review-work/references/severity.md).

## Verdicts

- **approve:** all criteria met, no blocker or major finding.
- **changes requested:** fix the findings and re-review.
- **reject:** the approach is wrong; re-plan or drop it.

A second review is needed after changes requested if any blocker was found.

Related: [definition of done](definition-of-done.md), [escalation](escalation.md), and the `review-work` skill.
