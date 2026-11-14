# Agents Skills Roles Oriented

A portable library of agent skills, with role charters that consume them. Built to be copied into an agent-ready repository, or installed directly into an agent's skills folder.

[![check](https://github.com/The-Urcydo/Agents-Skills-Roles-Oriented/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/The-Urcydo/Agents-Skills-Roles-Oriented/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/github/license/The-Urcydo/Agents-Skills-Roles-Oriented)](LICENSE)
[![Security policy](https://img.shields.io/badge/security-policy-blue)](SECURITY.md)

This repo is the skills-focused sibling of [Repo-Template](https://github.com/The-Urcydo/Repo-Template). Repo-Template owns the runnable project skeleton: docs, work items, roles, protocols, tools. This repo owns the skill library and the role charters that use it. Skills developed here are ported into Repo-Template when they are ready; Repo-Template is not modified from this repo.

**Status:** v0.1 in progress. Batch 0 established the contract and checker; Batch 1 added the catalog, scaffold, installer, and `write-skill`; Batch 4 ported the Repo-Template role charters, eight skills, and five protocols; Batch 5 ports the newer charter/method split, adds optional role fields, writes the porting guide, adds `plan-work`, and adds `workflow-lint`.

## Quick start

```bash
python3 tools/check.py
python3 tools/catalog.py --check
python3 -m unittest discover -s tools/tests -v
```

Install a skill into a project:

```bash
python3 tools/install.py --target claude --skill write-skill --project path/to/project
```

`check.py` validates the repository. `--strict` makes warnings fail. The test suite covers the tools.

## Layout

| Path | Purpose |
|---|---|
| `skills/` | The library. One flat folder per skill: `skills/<name>/SKILL.md` |
| `SKILLS.md` | Generated catalog of every skill, grouped by category |
| `roles/` | Role charters. Each charter lists the skills it uses; skills stay role-agnostic |
| `roles/ROSTER.md` | Generated table of roles, tiers, and skills. Do not hand-edit |
| `agents/` | The harness around the skills: protocols; adapters and evals are placeholders |
| `docs/` | The skill contract, the reasoning, authoring guides, and decisions |
| `tools/` | Standard-library Python: validation, catalog, scaffolding, installation |
| `.github/` | CI, ownership, and the pull-request template |

## What a skill is

A skill is a folder with a `SKILL.md` file. The front matter holds `name` and `description`; the body holds the procedure. Optional `references/`, `scripts/`, and `assets/` folders carry detail that is loaded only when needed.

```text
skills/code-review/
├── SKILL.md
└── references/
    └── severity.md
```

The open format is specified at [agentskills.io](https://agentskills.io/specification). This repo keeps the source in that format and puts tool-specific behavior in generated adapters, so the same skill works in Claude Code, OpenCode, and other agents.

Start with [docs/INDEX.md](docs/INDEX.md). The generated [SKILLS.md](SKILLS.md) lists every available skill.

## Roles

The library also carries eight role charters: orchestrator, planner, builder, reviewer, scribe, architect, researcher, and the optional security role. A charter says who is acting, what it reads, which skills it uses, and when it stops; the procedure stays in the skill. A charter may also declare `access: read-only` and `use_when`; see [the role format](docs/reference/role-format.md). See the generated [role roster](roles/ROSTER.md) and [roles/README.md](roles/README.md).

## Relationship to Repo-Template

- **Repo-Template** gives a new project its structure: docs, work items, role charters, protocols, and tools.
- **This repo** gives agents their procedures: a curated, validated skill library, plus role charters that say which skills each role uses.
- **Bootstrap:** the first port imported the Repo-Template harness as this library's starting point (ADR 0007). From here, new skills are developed here and ported back into Repo-Template.
- **Porting:** the mapping is in [the porting guide](docs/how-to/port-to-repo-template.md). It covers the shared-vs-role-local skill lane, front matter conversion, role fields, protocols, and docs front matter. The first port is recorded in [ADR 0007](docs/decisions/0007-port-the-agent-roles-and-skills.md); the charter/method split is recorded in [ADR 0009](docs/decisions/0009-split-role-routing-from-skill-method.md).

## Security

Report vulnerabilities privately under [SECURITY.md](SECURITY.md). Secret scanning, push protection, and private vulnerability reporting are enabled. CodeQL scans GitHub Actions and Python; its checks are required on `main`.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md). Every pull request needs a code owner's approval; the `*` catch-all in `.github/CODEOWNERS` covers every path. One topic per pull request, with evidence.

Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).

## License

MIT. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
