---
title: Port the agent roles and skills from Repo-Template
status: accepted
date: 2026-11-10
summary: Bring the eight Repo-Template role charters, eight portable skills, and five protocols into this flat library, adapted to the skill contract.
---
# 0007: Port the agent roles and skills from Repo-Template

## Context

Repo-Template ships `template/agents/`: eight role charters, five shared skills, five protocols, eight golden tasks, and an adapter generator. This repository is the skill library that Repo-Template draws from. It had the contract, checker, catalog, installer, and `write-skill`, but only one skill and placeholders for roles, protocols, adapters, and evals.

Copying the Repo-Template harness as-is would not work. Its skills use `disable-model-invocation`, omit `license` and `metadata`, and contain a `**Role:**` line; those are invalid or role-coupled under the local contract. The charters assume `work/items/` and `tools/transition.py`, and this repository deliberately does not carry a work state machine (ADR 0001). Repo-Template groups role-exclusive skills under the role bundle (its ADR 0005); this repository keeps one flat library and role-agnostic skills (ADRs 0002 and 0005).

## Decision

Port the harness with these changes:

- **Roles:** all eight charters: orchestrator, planner, builder, reviewer, scribe (flow); architect, researcher (advisory); security (optional). Each uses only the local charter keys and lists the skills it consumes. The procedure stays in `SKILL.md`.
- **Skills:** four shared procedures (`new-work-item`, `write-handoff`, `merge-work`, `write-doc`) and four role procedures (`review-work`, `record-decision`, `research-question`, `review-security`). Each uses the open front matter, states what it does and when, keeps the body role-agnostic, and puts the exact Repo-Template commands in a labeled "In Repo-Template" section.
- **Protocols:** definition of done, escalation, handoff, parallel work, and review. They are host-agnostic; the host supplies the tracker and paths.
- **Tooling:** `tools/roster.py` generates `roles/ROSTER.md`; `check.py` validates role front matter, tiers, role/folder names, listed skills, and roster drift.
- **Dropped:** `tailor-template`. It fills Copier placeholders and cuts modules, and this repository is not a Copier template (ADR 0001).
- **Deferred:** the eight golden evals and the adapter generator. They need harness infrastructure that does not exist here yet; `agents/evals/` and `agents/adapters/` remain placeholders.

The source is Repo-Template at commit `c0ab1a8` (MIT). This is a first-party port by the same owner, so no third-party `PROVENANCE.md` is added; this record is the provenance.

## Consequences

- The library has nine skills and eight role charters; every skill validates and every charter lists only existing skills.
- Repo-Template can copy the skills into `agents/skills/` and map the charters into its role bundles. The "In Repo-Template" sections name the exact commands.
- Maintenance grows: a change to a procedure now has to be checked against both the portable body and the host section.
- The flat layout stays intact. A skill used by more than one role remains in the shared library; the roster shows the shared use.
- Evals and adapters are still missing, so discovery and generated tool files are not yet measured or produced here.
- No `work/` state machine, no Copier, and no changes to Repo-Template are introduced.

## Alternatives considered

- **Copy the harness unchanged.** Rejected: invalid front matter, role logic in skills, and paths that do not exist here.
- **Keep role bundles.** Rejected: it conflicts with ADRs 0002 and 0005 and makes cross-role reuse a copy.
- **Port only the shared skills.** Rejected: the review, decision, research, and security procedures would stay duplicated in the charters.
- **Port evals and adapters now.** Rejected: it expands the batch into two new subsystems before the roles and skills are usable.

## Confirmation

- `python3 tools/check.py --strict` passes with 9 skills and 8 roles.
- `python3 tools/roster.py --check` reports the roster is up to date.
- The unit tests pass.
- No `SKILL.md` source sets `disable-model-invocation` or contains a `**Role:**` line.

## More information

- [Role roster](../../roles/ROSTER.md)
- [Roles guide](../../roles/README.md)
- [Protocols](../../agents/protocols/README.md)
- [Skill catalog](../../SKILLS.md)
- [Add a role](../how-to/add-a-role.md)
