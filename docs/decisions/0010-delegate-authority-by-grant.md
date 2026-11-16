---
title: Delegate authority by grant, not by role
status: proposed
date: 2026-11-16
summary: Handle delegated authority with a grant rule in the escalation protocol, one pointer in the root rules, and an independence rule in the review protocol, and add no advisor role.
---
# 0010: Delegate authority by grant, not by role

## Context and problem statement

The owner works in layers. The owner decides. An advisor session gives an independent view and drafts briefs. An orchestrator session does the work and opens the pull request. On 2026-11-15 the owner agreed that an advisor may hold delegated authority, not authority equal to the owner's, and asked whether the harness needs an `advisor` role.

Three questions had no answer in the repository:

- **What is delegated, and how is it revoked?** The [`merge-work`](../../skills/merge-work/SKILL.md) skill defines a grant for merging only. Nothing says what else an agent may do for the human, for how long, or what no grant can unlock.
- **Who checks the result of a brief?** [The review protocol](../../agents/protocols/review.md) bars the builder from reviewing its own work. It does not bar the author of the brief, who then judges whether the brief was followed.
- **Where would a rule be read?** No role charter links a file in `agents/protocols/`, so a rule that lives only in a protocol may never be loaded. The root [`AGENTS.md`](../../AGENTS.md) is always loaded, and the checker caps its length.

Earlier advisor sessions showed three failure modes. The author of a brief was also its only independent reviewer, and a hardcoded count reached two pull request descriptions. A compaction summary drifted from the facts. Text from other agents' reports, score sheets, and web pages was taken for instruction. These come from the owner's session notes. This repository holds no second source for them, so treat them as a lead.

## Decision drivers

- One fact, one home: `merge-work` already defines a grant, so reuse its definition instead of forking it.
- Routing and limits belong in a charter or a protocol, never in a skill ([harness rules](../../agents/AGENTS.md)).
- Protocols stay host-agnostic: no tool, model, or account names.
- Instruction text has a cost ([ADR 0009](0009-split-role-routing-from-skill-method.md)): move or merge existing text before adding new text.
- A rule that no agent reads changes nothing.
- A new role must pass the admission test in [roles/README.md](../../roles/README.md).

## Considered options

- **Add an `advisor` role** in the advisory tier.
- **Add the rules to the escalation and review protocols only.**
- **Add the rules to the protocols and one pointer in the root `AGENTS.md`.**
- **Put the whole rule in the root `AGENTS.md`.**
- **Add a new `delegation.md` protocol.**
- **Change nothing** and keep the rules in the owner's session notes.

## Decision outcome

Chosen option: **add the rules to the existing protocols, add one pointer in the root `AGENTS.md`, and add no role.**

1. **The admission test is not met.** Every artifact the advisor produces already has an owner: briefs (planner), decisions (architect), source checks (researcher), independent review (reviewer), and the human's short queue with a recommendation, a default, and a cost (orchestrator). The `access` field has two values, and the researcher, the reviewer, and the security role already use `read-only`; what is new here is authority, not tool access. An advisor that writes a brief and judges its result is the maker and the checker at once, the opposite of the checker half the test asks for. Only the context-window criterion is partly met, and a separate session already covers it.
2. **Delegation is of work, not of authority.** The human's request, or a brief the human hands over, authorizes the work it names, up to the hand-over for review. An advisor session holds no authority of its own: a brief it drafts authorizes work only once the human hands it over, and it cannot pass a grant to another session. Any other action on shared state needs a grant. The human keeps approving a pull request, pushing to the default branch, changing branch protection, accepting a security risk, and accepting a decision record.
3. **Grants.** The [escalation protocol](../../agents/protocols/escalation.md) gains a "Grants and delegation" section. A grant is the human's own words, in the session or in a record the human wrote, as `merge-work` already defines it. It covers one action, only what can be undone, and ends when the action is done, on "stop", or when the session that heard it ends. Merging stays under `merge-work` and the host's rule on who may merge. The governance acts above join the existing "Other decisions" list instead of a new list.
4. **Independence.** The review protocol gains one bullet: an important item is reviewed by a fresh session that did not write or shape the brief, and the reviewer recomputes counts and file lists from the repository.
5. **One pointer in the root rules.** `AGENTS.md` gains hard rule 13: one line that says grants come only from the human's own words and points to the escalation protocol. The owner approved this root-rule change on 2026-11-16. It is the only text this decision adds to an always-loaded file.
6. **No rename.** The planner keeps its name; it already owns the brief.

## Consequences

- Good: the grant rule reuses the definition `merge-work` already has. There is no new role, so the roster, `SKILLS.md`, the tools, and the tests do not change. The pointer in `AGENTS.md` reaches every agent that loads it.
- Bad: the change adds instruction text to a protocol and to the root rules and removes none; the pull request reports the measured words. A protocol binds less than a charter's `never` list. The repository cannot verify that quoted words are the human's, so the host session must. No checker stops an agent that skips the rule.
- Bad: `merge-work` lets the owner's words grant a merge, while `CONTRIBUTING.md` says accounts used to drive unattended agent sessions never merge. That tension predates this decision. This decision does not resolve it: the protocol defers to both and widens neither.
- Neutral: any change under `agents/` or to the root rules still needs the owner's approval ([harness rules](../../agents/AGENTS.md)).

## Confirmation

- The four repository checks pass: `python3 tools/check.py --strict`, `python3 tools/catalog.py --check`, `python3 tools/roster.py --check`, and `python3 -m unittest discover -s tools/tests`.
- Acceptance gate: do not move this record to `accepted` until one of these has happened, whichever comes first:
  - a tabletop run, in which a fresh session is given only the protocols and the root rules and answers each scenario in the pull request, and the owner compares the answers with the expected behavior;
  - the first real delegation that uses the rule, where a reviewer in a fresh session checks that the grant is quoted in the handoff and that the brief's counts match the repository.
- Revisit this decision, and consider a role, if another agent must route to an advisor by name, if an adapter should enforce an advisor's `never` list, or if a real case shows the existing roles failed.
- Not verified: that an agent follows these rules better than before. The evals module is still a placeholder, the same limit [ADR 0009](0009-split-role-routing-from-skill-method.md) records. The failure modes above rest on one set of session notes.

Review by: 2027-02-15, or at the next model generation if sooner.

## Pros and cons of the options

### Add an `advisor` role

- Good: a named seat that agents can route to, and a `never` list that a future adapter could enforce.
- Bad: it fails the admission test; it adds a charter and a roster row to keep in step across the docs; the authority question stays open because `access` cannot express it; the name is easy to confuse with the `advisory` tier.

### Add the rules to the escalation and review protocols only

- Good: the smallest change to the text.
- Bad: no charter links a protocol file, so an agent may never read the rule; a protocol binds less than a charter.

### Add the rules to the protocols and one pointer in the root `AGENTS.md`

- Good: the pointer reaches every agent that loads `AGENTS.md`, and the detail has one home.
- Bad: one more line in an always-loaded file whose length is capped; the rule still binds less than a charter, and no checker enforces it.

### Put the whole rule in the root `AGENTS.md`

- Good: it is always loaded.
- Bad: it takes several lines of a capped file, and it splits the escalation rules between the root file and a protocol.

### Add a new `delegation.md` protocol

- Good: one page holds the whole rule.
- Bad: a new file means updating several lists of protocols, and nothing would link to it; the same rule fits in the escalation protocol.

### Change nothing

- Good: no new instruction text.
- Bad: the rules stay in a private session that local agents cannot see, and the same failure modes can repeat.

## More information

- Related: [ADR 0002](0002-roles-consume-skills.md), [ADR 0006](0006-repository-governance.md), [ADR 0008](0008-single-owner-organization-access.md), and [ADR 0009](0009-split-role-routing-from-skill-method.md).
- This record stays `proposed` until the owner accepts it, after the acceptance gate above.
