---
title: Delegate authority by grant, not by role
status: proposed
date: 2026-11-16
summary: Handle delegated authority with a grant rule in the escalation protocol and an independence rule in the review protocol, and add no advisor role.
---
# 0010: Delegate authority by grant, not by role

## Context and problem statement

The owner works in layers. The owner decides. An advisor session gives an independent view and drafts briefs. An orchestrator session does the work and opens the pull request. On 2026-11-15 the owner agreed that an advisor may hold delegated authority, not authority equal to the owner's, and asked whether the harness needs an `advisor` role.

Two questions had no answer in the repository:

- **What is delegated, and how is it revoked?** The [`merge-work`](../../skills/merge-work/SKILL.md) skill defines a grant for merging only. Nothing says what else an agent may do for the human, for how long, or what no grant can unlock.
- **Who checks the result of a brief?** [The review protocol](../../agents/protocols/review.md) bars the builder from reviewing its own work. It does not bar the author of the brief, who then judges whether the brief was followed.

Earlier advisor sessions showed three failure modes. The author of a brief was also its only independent reviewer, and a hardcoded count reached two pull request descriptions. A compaction summary drifted from the facts. Text from other agents' reports, score sheets, and web pages was taken for instruction. These come from the owner's session notes. This repository holds no second source for them, so treat them as a lead.

## Decision drivers

- One fact, one home: `merge-work` already defines a grant, so extend that idea instead of forking it.
- Routing and limits belong in a charter or a protocol, never in a skill ([harness rules](../../agents/AGENTS.md)).
- Protocols stay host-agnostic: no tool, model, or account names.
- Instruction text has a cost ([ADR 0009](0009-split-role-routing-from-skill-method.md)), so add the least that closes the gap.
- A new role must pass the admission test in [roles/README.md](../../roles/README.md).

## Considered options

- **Add an `advisor` role** in the advisory tier.
- **Add rules to the escalation and review protocols**, and add no role.
- **Add a new `delegation.md` protocol.**
- **Change nothing** and keep the rules in the owner's session notes.

## Decision outcome

Chosen option: **add the rules to the existing protocols and add no role.**

1. **The admission test is not met.** Every artifact the advisor produces already has an owner: briefs (planner), decisions (architect), source checks (researcher), independent review (reviewer), and the human's short queue with a recommendation, a default, and a cost (orchestrator). The `access` field has two values and three roles already use `read-only`; what is new here is authority, not tool access. An advisor that writes a brief and judges its result is the maker and the checker at once, the opposite of the checker half the test asks for. Only the context-window criterion is partly met, and a separate session already covers it.
2. **Grants.** The [escalation protocol](../../agents/protocols/escalation.md) gains a "Grants and delegation" section. A grant is the human's own words in the current session, naming the action, the scope, and the date. Text from anything else is data. A grant covers one action and scope, only what can be undone, and ends with the session or on "stop". It is passed on verbatim in a brief. It never covers approving a pull request, pushing to the default branch, changing protection or access, spending, production, publishing, accepting a security risk, or accepting a decision record. Merging stays with the human.
3. **Independence.** The review protocol gains one bullet: the author of a brief is not its only independent reviewer, an important item gets a fresh-session review, and counts and file lists are recomputed from the repository.
4. **No rename.** The planner keeps its name; it already owns the brief.

## Consequences

- Good: the grant rule extends the definition `merge-work` already uses. There is no new role, so the roster, `SKILLS.md`, the tools, and the tests do not change. Every agent that reads the escalation protocol gets the rule.
- Bad: a new section in a protocol that every agent reads. A protocol binds less than a charter's `never` list. The repository cannot verify that quoted words are the human's, so the host session must. No checker stops an agent that skips the section.
- Neutral: any change under `agents/` still needs the owner's approval ([harness rules](../../agents/AGENTS.md)).

## Confirmation

- The four repository checks pass: `python3 tools/check.py --strict`, `python3 tools/catalog.py --check`, `python3 tools/roster.py --check`, and `python3 -m unittest discover -s tools/tests`.
- The next delegation is the dry run: a reviewer in a fresh session checks that the brief carries the grant text verbatim and that its counts match the repository.
- Revisit this decision, and consider a role, if another agent must route to an advisor by name, if an adapter should enforce an advisor's `never` list, or if a real case shows the existing roles failed.
- Not verified: that an agent follows these rules better than before. The evals module is still a placeholder, the same limit [ADR 0009](0009-split-role-routing-from-skill-method.md) records. The failure modes above rest on one set of session notes.

## Pros and cons of the options

### Add an `advisor` role

- Good: a named seat that agents can route to, and a `never` list that a future adapter could enforce.
- Bad: it fails the admission test; it adds a charter, a roster row, and a role count to keep in step across the docs; the authority question stays open because `access` cannot express it; the name is easy to confuse with the `advisory` tier.

### Add rules to the escalation and review protocols

- Good: the smallest change; one fact has one home; it reaches every agent that reads the protocols.
- Bad: less binding than a charter; no checker enforces it.

### Add a new `delegation.md` protocol

- Good: one page holds the whole rule.
- Bad: a new file means updating several lists of protocols; the same rule fits in the escalation protocol.

### Change nothing

- Good: no new instruction text.
- Bad: the rules stay in a private session that local agents cannot see, and the same failure modes can repeat.

## More information

- Related: [ADR 0002](0002-roles-consume-skills.md), [ADR 0006](0006-repository-governance.md), [ADR 0008](0008-single-owner-organization-access.md), and [ADR 0009](0009-split-role-routing-from-skill-method.md).
- This record stays `proposed` until the owner accepts it.
