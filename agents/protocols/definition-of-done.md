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
- [ ] The docs-for-the-scribe decision is settled: the builder recorded it and the reviewer checked it against the diff. The format is in `write-handoff`; the reviewer charter holds the routing.

## For items that change behavior, or whose builder listed docs

- [ ] Affected docs are updated.
- [ ] The changelog has a line under the unreleased section.
- [ ] Generated files are in sync.

An item whose builder recorded that no docs changed and whose review agreed needs no docs and no changelog line.

## For full items

- [ ] The review exists, written by an agent other than the one that built it, with a verdict and per-criterion evidence.
- [ ] No blocker or major finding is left open.
- [ ] A required security review exists and its blocker or major findings are fixed or accepted by the human.

## Not done if

- You cannot show evidence for a claim.
- A check was skipped "because it is unrelated".
- Placeholders or unfinished markers were introduced and not tracked in a new item.
- The docs decision was guessed instead of checked against the diff.

Related: [review](review.md), [handoff](handoff.md), and the [skill format](../../docs/reference/skill-format.md).
