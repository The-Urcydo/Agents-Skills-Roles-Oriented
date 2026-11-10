# Agents Skills Roles Oriented

A portable library of agent skills, with role charters that consume them. Built to be copied into an agent-ready repository, or installed directly into an agent's skills folder.

This repo is the skills-focused sibling of [Repo-Template](https://github.com/The-Urcydo/Repo-Template). Repo-Template owns the runnable project skeleton: docs, work items, roles, protocols, tools. This repo owns the skill library and the role charters that use it. Skills developed here are ported into Repo-Template when they are ready; Repo-Template is not modified from this repo.

**Status:** v0.1 in progress. Batch 0 established the contract and checker; Batch 1 adds the catalog, scaffold, installer, and the first skill (`write-skill`).

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
| `agents/` | The harness around the skills: protocols, generated adapters, optional evals |
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

Start with [docs/INDEX.md](docs/INDEX.md).

## Available skills

- [`write-skill`](skills/write-skill/SKILL.md): create or revise a skill in this library.

## Relationship to Repo-Template

- **Repo-Template** gives a new project its structure: docs, work items, role charters, protocols, and tools.
- **This repo** gives agents their procedures: a curated, validated skill library, plus role charters that say which skills each role uses.
- **Porting:** copy `skills/<name>/` into Repo-Template's `agents/skills/<name>/`; map `roles/<role>/ROLE.md` into Repo-Template's role bundle. The porting guide arrives in Batch 5.

## Contributing

Changes to `skills/`, `roles/`, `agents/`, `tools/`, or `.github/` need the owner's approval, like Repo-Template's harness rules. One topic per pull request, with evidence. Read [AGENTS.md](AGENTS.md) before you start.

## License

MIT. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
