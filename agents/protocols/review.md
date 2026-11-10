# Review protocol

Independent review is the main quality gate in a repo with no human in the loop for every change.

## Independence

- The agent doing the review is never the agent that built the item. With a single model playing both parts, use a fresh session with no memory of the build, and read the brief before the author's summary.
- The review does not fix findings. Fixing makes the review a second builder and removes the second pair of eyes.

## Procedure

1. Read the brief, then the handoff, then the diff. Note anything the diff changes that the brief did not ask for.
2. Run the checks yourself.
3. For each acceptance criterion, verify it and record the evidence. "Looks right" is not evidence.
4. Check the rules: decisions respected, ownership respected, generated files in sync, docs updated.
5. Write the review: verdict, per-criterion results, findings ranked by severity.

## Findings

| Severity | Meaning | Effect |
|---|---|---|
| blocker | Wrong, unsafe, or breaks a rule or an accepted decision | Must fix before approval |
| major | Meets the letter but misses the intent, or is fragile | Must fix or be accepted by the human |
| minor | Style, naming, or a small improvement | Fix now or log a new item |

Each finding states: what, where, why it matters, and a recommended fix.

## Verdicts

- **approve:** all criteria met, no blocker or major finding.
- **changes requested:** fix the findings and re-review.
- **reject:** the approach is wrong; re-plan or drop it.

A second review is needed after changes requested if any blocker was found.

Related: [definition of done](definition-of-done.md), [escalation](escalation.md), and the `review-work` skill.
