---
title: Split role routing from skill method
status: accepted
date: 2026-11-14
summary: Port the Repo-Template charter/method split so role charters hold routing and limits while skills hold procedure, without importing the work tracker or the role-local skill layout.
---
# 0009: Split role routing from skill method

## Context and problem statement

[ADR 0002](0002-roles-consume-skills.md) made roles consume a flat, role-agnostic skill library. [ADR 0007](0007-port-the-agent-roles-and-skills.md) ported the first eight charters, eight skills, and five protocols from Repo-Template at commit `c0ab1a8`. The charters pointed at skills but left two things unresolved:

- **Routing was implicit.** The reviewer had no rule for a required security review, no rule for who acts after approval, and no way to skip the scribe when no docs changed. The builder had no single line the reviewer could route on.
- **The contract was underspecified.** A role could declare `skills` but not whether it was read-only or when a callable role should be picked. Repo-Template's newer harness added `access` and `use_when` for exactly those two facts.

Repo-Template's current `main` (`a9233bf`, tag `v0.3.5`) records its own answer in [ADR 0009](https://github.com/The-Urcydo/Repo-Template/blob/main/template/docs/decisions/0009-split-each-role-into-a-charter-and-skills.md): `ROLE.md` holds routing and limits, a skill holds the method, and one fact has one home. Its full diff since our last port is 80 files, +3,552/−163; the harness files that matter here are 42 files, +1,147/−90, almost entirely under `template/agents/` and `template/docs/dev/`. It adds no new shared skill. The only shared Repo-Template skill this library lacks is `tailor-template`, and it is Copier-specific; its role-local `verify-work` and `review-change` have equivalents here in `review-work` and `review-security`.

This repository cannot copy that answer literally. It has no `work/` state machine (ADR 0001), no `item_files`/`writes_files` ownership model, and no role-local skill folders (ADRs 0002 and 0005). The question is what to take and what to leave.

## Decision drivers

- One fact, one home: a change to a flow should be one edit.
- What must never be skipped belongs in the file an agent always reads: the charter.
- The skill library stays flat and role-agnostic so a skill can be installed into any project and used by any role.
- The repository stays tracker-agnostic; the host supplies its work tracker and state names.
- Instruction text has a cost, so move or merge existing text before adding new text.
- No adapter generator exists yet, so a new role field must be declarative and honest about not being enforced.

## Considered options

- **Copy Repo-Template wholesale.** Take role-local skill folders, `item_files`, `writes_files`, the work tracker, and the Copier files.
- **Keep the current charters and add only `access`/`use_when`.** A small change, but the reviewer and builder routing stays missing.
- **Adopt the split, keep the flat library, and port only the routing.** Add the two optional fields, put routing in charters and protocols, keep methods in skills, and leave the tracker, role-local layout, and template machinery out.
- **Move all procedure into the charters.** The shortest skill library, but every role run pays for method it may not need, and the skills lose their portability.

## Decision outcome

Chosen option: **adopt the split, keep the flat library, and port only the routing.**

1. **`ROLE.md` is the charter.** It holds the front matter, when the role runs or is called, ownership, routing (every rule that changes who owns an item or its status), the quality bar, and a pointer to its skills.
2. **A skill is the method for one task.** It holds the read order, checks, templates, evidence, and commands that do not move an item. It never holds a role name or routing.
3. **One fact, one home.** When both need a fact, the charter states the rule and the skill points to it. A skill that only restates its charter is not added.
4. **`access` and `use_when` are optional charter fields.** `access` is `full` (the default) or `read-only`; it is a tool-neutral hint, and the `never` list remains binding. `use_when` completes "Use when ..." for a role that is called and does not own the flow. The researcher and architect set `use_when`; the researcher, reviewer, and security role are `read-only`.
5. **The routing is ported.** The reviewer routes a required security review to the security role before any verdict, and routes a confirmed `Docs for the scribe: none, behavior unchanged.` item to the orchestrator after approval. The builder writes the docs line. The scribe skips a confirmed `none`. The orchestrator closes it. The handoff protocol gains a reference state machine.
6. **The flat library stays.** Role-local skill folders, `item_files`, and `writes_files` are not adopted. A role lists the shared skills it uses; the library remains flat under `skills/`.
7. **The template machinery stays out.** Copier, `work/`, `tools/transition.py`, `new_item.py`, `question.py`, `worktree.py`, `tailor-template`, and docs front matter are not ported. Adapters and evals remain separate batches.

## Consequences

- Good: a flow change is one edit; routing sits in the always-read charter; skills remain portable; the repository stays tracker-agnostic; the new fields are validated by the checker.
- Bad: a charter alone no longer shows the whole procedure; an agent that skips the skill misses the method; `access` is declarative until an adapter enforces it; porting a role back to Repo-Template needs the mapping in the porting guide.
- Neutral: `roles/ROSTER.md` and `SKILLS.md` do not change unless a skill is added; the front matter parser and the roster keep working because the new fields are optional.

## Confirmation

- `python3 tools/check.py --strict` validates `access` and `use_when` and still passes the eight charters.
- `tools/tests/test_tools.py` covers a valid `read-only` role, an invalid access value, a valid `use_when`, and an empty one.
- `agents/protocols/` holds the routing, and each charter points at its skills instead of copying them.
- `docs/how-to/port-to-repo-template.md` maps the flat fields and skills back to Repo-Template's role bundles.
- Not verified: that a real agent follows the routing better. The evals module is still a placeholder; this is the same limit Repo-Template records for its own harness.

## Pros and cons of the options

### Copy Repo-Template wholesale

- Good: no adaptation work; identical harness.
- Bad: imports the work tracker and Copier machinery this repository deliberately left behind; role-local skills break the flat library; `item_files`/`writes_files` have no meaning here.

### Add only `access`/`use_when`

- Good: smallest diff.
- Bad: keeps the missing reviewer and builder routing; the fields describe access but not what happens next.

### Adopt the split, keep the flat library, port only the routing

- Good: fixes the missing routing, keeps the library portable, and stays honest about what is not enforced.
- Bad: two files to read for the whole procedure; the porting guide must translate the differences.

### Move all procedure into the charters

- Good: one file per role.
- Bad: every role run pays for method it may not need; skills lose their portability; the flat library becomes decorative.

## More information

- Repo-Template source: [`a9233bf`](https://github.com/The-Urcydo/Repo-Template/commit/a9233bfcc0693bf1c51f82d39d5e2e07390f837a), tag `v0.3.5`.
- Repo-Template ADR 0009: [Split each role into a charter and skills](https://github.com/The-Urcydo/Repo-Template/blob/main/template/docs/decisions/0009-split-each-role-into-a-charter-and-skills.md).
- Related: [ADR 0001](0001-skills-first-library.md), [ADR 0002](0002-roles-consume-skills.md), [ADR 0005](0005-flat-skills-layout.md), [ADR 0007](0007-port-the-agent-roles-and-skills.md), [the role format](../reference/role-format.md), and [the porting guide](../how-to/port-to-repo-template.md).
