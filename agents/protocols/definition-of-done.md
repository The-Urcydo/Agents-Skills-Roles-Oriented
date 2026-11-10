# Definition of done

An item is done only when all of these are true. The tools check the mechanical ones; the role charters check the rest.

## For every item

- [ ] Every acceptance criterion is met, and each has evidence: a command run, a file, or a link.
- [ ] The repository's check passes.
- [ ] The tests the project defines pass; new behavior has tests.
- [ ] The handoff is current: state, next action, evidence, decisions, and dead ends.
- [ ] No file was changed outside the role's lane without the owner's handoff.
- [ ] No accepted decision was contradicted. If one had to change, a superseding record exists.
- [ ] Generated files were regenerated, not hand-edited.

## For items that change behavior

- [ ] Affected docs are updated.
- [ ] The changelog has a line under the unreleased section.
- [ ] Generated files are in sync.

## For full items

- [ ] The review exists, written by an agent other than the one that built it, with a verdict and per-criterion evidence.
- [ ] No blocker or major finding is left open.

## Not done if

- You cannot show evidence for a claim.
- A check was skipped "because it is unrelated".
- Placeholders or unfinished markers were introduced and not tracked in a new item.

Related: [review](review.md), [handoff](handoff.md), and the [skill format](../../docs/reference/skill-format.md).
