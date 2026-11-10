# Agents-Skills-Roles-Oriented

A portable library of agent skills plus the role charters that consume them. The human owner decides; agents propose in pull requests.

## Commands

- Check everything: `python3 tools/check.py`
- Strict check (warnings fail): `python3 tools/check.py --strict`
- Test the tools: `python3 -m unittest discover -s tools/tests -v`
- Scaffold a skill: `python3 tools/new_skill.py <name> --category <category>`
- Regenerate the catalog: `python3 tools/catalog.py`
- Verify the catalog: `python3 tools/catalog.py --check`
- Install into an agent: `python3 tools/install.py --target <claude|opencode|agents> --skill <name> --project <path>`

## Where things are

- `skills/<name>/SKILL.md`: the canonical skill library. Flat, one folder per skill.
- `SKILLS.md`: generated catalog. Do not hand-edit it.
- `roles/<role>/ROLE.md`: a role charter. It lists the skills the role uses; it does not own them.
- `agents/`: protocols, generated adapters, optional evals. Not the skill library. Adapter sync (`tools/sync_adapters.py`) arrives in Batch 4.
- `docs/`: the skill contract (`docs/reference/skill-format.md`), reasoning, how-tos, and decisions.
- `tools/`: standard-library Python. Tests live in `tools/tests/`.

## Hard rules

1. **Open format first.** A `SKILL.md` source uses only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Tool-specific fields belong in generated adapters, not in the source.
2. **One flat skill folder.** The folder name equals `name`; names are unique, lowercase, and hyphenated. No category folders.
3. **No role logic in a skill.** A skill says what to do. A role charter says when that role uses it.
4. **Imports carry provenance.** Every third-party skill has a `PROVENANCE.md` with the source URL, commit, license, and changes. Add it to `THIRD_PARTY_NOTICES.md`.
5. **Never hand-edit generated files.** `SKILLS.md`, `roles/ROSTER.md`, and adapter outputs are generated. Edit the source and re-run the generator.
6. **Owner approval.** Changes under `skills/`, `roles/`, `agents/`, `tools/`, `.github/`, or this file need the owner's approval in a pull request.
7. **No secrets or personal paths.** Skills are public instructions; never put credentials, tokens, or absolute home paths in them.
8. **Do not modify Repo-Template from this repo.** Porting is a separate, explicit change in Repo-Template.
9. **Evidence before handoff.** Run `python3 tools/check.py` and, when `tools/` changed, the unit tests. Put the command and result in the pull request.
10. **Scripts need documentation.** A skill that runs code must state its runtime, dependencies, and whether it needs network access.

## Adding a skill

1. Read `docs/reference/skill-format.md`.
2. Create the folder with `python3 tools/new_skill.py <name> --category <category>`, or create `skills/<name>/SKILL.md` by hand.
3. Write a description that says what the skill does and when to use it.
4. Add `references/`, `scripts/`, or `assets/` only if the skill needs them.
5. Run `python3 tools/catalog.py` and `python3 tools/check.py --strict`.
6. Open a pull request with the check output and a one-line summary.

## Work tracking

There is no `work/` state machine in this repo. Use GitHub issues for proposals and pull requests for changes. A skill is done when it validates, is reviewed, and has evidence that it works.
