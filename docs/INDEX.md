# Documentation index

Start here. This file is the map; open only what the task needs.

## Contract

- [Skill format](reference/skill-format.md): required front matter, folder shape, metadata, and quality rules.
- [Role format](reference/role-format.md): required and optional charter fields, and the charter/skill split.
- [Why skills](explanation/why-skills.md): the context-budget reason for skills, and how they differ from roles and `AGENTS.md`.

## Catalog

- [Skills catalog](../SKILLS.md): generated list of every skill, grouped by category.

## Roles and protocols

- [Roles](../roles/README.md): what a charter contains, the tiers, and how to add one.
- [Role roster](../roles/ROSTER.md): generated table of roles, skills, and shared use.
- [Protocols](../agents/protocols/README.md): handoff, review, escalation, definition of done, and parallel work.
- [Harness rules](../agents/AGENTS.md): rules for changing roles, protocols, adapters, and evals.

## Project

- [Contributing](../CONTRIBUTING.md): setup, checks, pull requests, and the merge policy.
- [Security policy](../SECURITY.md): how to report a vulnerability privately.
- [Code of conduct](../CODE_OF_CONDUCT.md): standards for humans and agents.

## Guides

- [Write a skill](how-to/write-a-skill.md): from idea to validated pull request.
- [Add a role](how-to/add-a-role.md): pass the admission test, write the charter, and regenerate the roster.
- [Install skills](how-to/install-skills.md): copy a skill into Claude Code, OpenCode, or `.agents/skills`.
- [Port to Repo-Template](how-to/port-to-repo-template.md): map a skill, role, protocol, or doc into the generated-project harness.

## Decisions

- [0001: Adopt a skills-first library](decisions/0001-skills-first-library.md)
- [0002: Roles consume skills](decisions/0002-roles-consume-skills.md)
- [0003: Curate third-party skills with provenance](decisions/0003-curated-imports-with-provenance.md)
- [0004: Open spec first, adapter extensions](decisions/0004-open-spec-with-adapter-extensions.md)
- [0005: Flat skills layout with a generated catalog](decisions/0005-flat-skills-layout.md)
- [0006: Protect main and report security privately](decisions/0006-repository-governance.md)
- [0007: Port the agent roles and skills from Repo-Template](decisions/0007-port-the-agent-roles-and-skills.md)
- [0008: Keep the single-owner, multi-machine organization access model](decisions/0008-single-owner-organization-access.md)
- [0009: Split role routing from skill method](decisions/0009-split-role-routing-from-skill-method.md)
- [Decision record rules](decisions/README.md)
