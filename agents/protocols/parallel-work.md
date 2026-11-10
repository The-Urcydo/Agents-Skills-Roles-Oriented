# Parallel work

Several agents at once is the normal case. Collisions are prevented by structure, not by hoping.

## Three mechanisms

1. **One writer per path.** Folder ownership and per-role file lanes mean two agents never write the same file. If you need a change in a path you do not own, say so in the handoff for the owner.
2. **One worktree per agent.** Each building agent works in its own git worktree on its own branch. Agents never share a working directory.
3. **Locked shared tools.** If the host has tools for creating items, allocating decision numbers, or editing the human queue, those tools take a file lock so two agents cannot allocate the same number or corrupt a file.

## What can run in parallel

- Items whose changes live in different folders or different files.
- Research and planning for different items.
- Review of one item while another is built.

## What must not

- Two items that edit the same code files, unless one is sequenced after the other: set the later one blocked on the earlier merge.
- Hand-editing generated files. Rebuild them from the source after merging.
- Two agents editing `AGENTS.md` or the role, protocol, and skill harness. Harness changes are serialized through the architect and the human.

## Merging

- Merging needs the owner's grant. Follow the `merge-work` skill.
- After merging, regenerate the generated files, then run the check.
- Remove the sibling worktree when the item is finished, but only after the branch is merged or abandoned.

Related: [handoff](handoff.md), [review](review.md), and the `merge-work` skill.
