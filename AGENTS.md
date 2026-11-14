# Agents-Skills-Roles-Oriented

A portable library of agent skills plus the role charters that consume them. The human owner decides; agents propose in pull requests.

## Commands

- Check everything: `python3 tools/check.py`
- Strict check (warnings fail): `python3 tools/check.py --strict`
- Test the tools: `python3 -m unittest discover -s tools/tests -v`
- Scaffold a skill: `python3 tools/new_skill.py <name> --category <category>`
- Regenerate the catalog: `python3 tools/catalog.py`
- Verify the catalog: `python3 tools/catalog.py --check`
- Regenerate the role roster: `python3 tools/roster.py`
- Verify the role roster: `python3 tools/roster.py --check`
- Install into an agent: `python3 tools/install.py --target <claude|opencode|agents> --skill <name> --project <path>`

## Where things are

- `skills/<name>/SKILL.md`: the canonical skill library. Flat, one folder per skill.
- `SKILLS.md`: generated catalog. Do not hand-edit it.
- `roles/<role>/ROLE.md`: a role charter. It lists the skills the role uses; it does not own them.
- `roles/ROSTER.md`: generated table of roles, tiers, and skills. Do not hand-edit it.
- `agents/protocols/`: rules between roles: handoff, review, escalation, definition of done, and parallel work. `agents/adapters/` and `agents/evals/` remain documented placeholders. `agents/AGENTS.md` holds the rules for changing the harness.
- `docs/`: the skill contract (`docs/reference/skill-format.md`), reasoning, how-tos, and decisions.
- `tools/`: standard-library Python. Tests live in `tools/tests/`.
- `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`: reporting, contribution, and conduct.

## Organization accounts

Every account in `The-Urcydo` belongs to the same owner, one per home machine:
`nguyenquocduyloc`, `NguyenLoc231`, `shiniroku`, and `shinkir6u`. The owner
drives agent sessions from those machines; they are not independent
maintainers. The owner's accounts keep organization owner roles so each machine
can create and work on repositories. The organization requires 2FA.
Accounts used to drive unattended agent sessions never approve a pull request or
hold a review role. The access tradeoff is recorded in
[ADR 0008](docs/decisions/0008-single-owner-organization-access.md).

## Hard rules

1. **Open format first.** A `SKILL.md` source uses only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Tool-specific fields belong in generated adapters, not in the source.
2. **One flat skill folder.** The folder name equals `name`; names are unique, lowercase, and hyphenated. No category folders.
3. **No role logic in a skill.** A skill says what to do. A role charter says when that role uses it.
4. **Imports carry provenance.** Every third-party skill has a `PROVENANCE.md` with the source URL, commit, license, and changes. Add it to `THIRD_PARTY_NOTICES.md`.
5. **Never hand-edit generated files.** `SKILLS.md`, `roles/ROSTER.md`, and adapter outputs are generated. Edit the source and re-run the generator.
6. **Owner approval.** Every pull request needs the approval of a code owner in `.github/CODEOWNERS`: `@nguyenquocduyloc` and `@NguyenLoc231`. The `*` catch-all covers every path, so every change needs it. Agent-operated accounts never approve. Do not push or force-push to `main`; merge with a merge commit, never squash-merge or rebase-merge.
7. **No secrets or personal paths.** Skills are public instructions; never put credentials, tokens, or absolute home paths in them.
8. **Do not modify Repo-Template from this repo.** Porting is a separate, explicit change in Repo-Template.
9. **Evidence before handoff.** Run `python3 tools/check.py --strict` and, when `tools/` changed, the unit tests. Put the command and result in the pull request.
10. **Scripts need documentation.** A skill that runs code must state its runtime, dependencies, and whether it needs network access.
11. **Report security problems privately.** Follow `SECURITY.md`; do not open a public issue with the details.
12. **Workflows are code.** Set `permissions` and pin every action to a full commit SHA.

## Adding a skill

1. Read `docs/reference/skill-format.md`.
2. Create the folder with `python3 tools/new_skill.py <name> --category <category>`, or create `skills/<name>/SKILL.md` by hand.
3. Write a description that says what the skill does and when to use it.
4. Add `references/`, `scripts/`, or `assets/` only if the skill needs them.
5. If a role uses it, add the name to that role's charter and regenerate the roster with `python3 tools/roster.py`.
6. Run `python3 tools/catalog.py` and `python3 tools/check.py --strict`.
7. Open a pull request with the check output and a one-line summary.

## Work tracking

There is no `work/` state machine in this repo. Use GitHub issues for proposals and pull requests for changes. The ported skills use the host repository's tracker; this repository's own work stays on GitHub. A skill is done when it validates, is reviewed, and has evidence that it works.
