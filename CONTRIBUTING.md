# Contributing

Thanks for your interest. This repository is a library of agent skills and role
charters. The human owner decides; agents and contributors propose in pull
requests.

The rules for working here are in [AGENTS.md](AGENTS.md). If this page and
`AGENTS.md` disagree, `AGENTS.md` wins.

## Before you start

- Found a bug or have an idea? Open an issue using the forms. Check the open
  issues first.
- Found a security problem? Do not open a public issue. Follow
  [SECURITY.md](SECURITY.md).
- By taking part, you agree to the [code of conduct](CODE_OF_CONDUCT.md).

## Set up

Requires Python 3.13 or newer and git. The tools use only the standard library;
there is nothing to install.

```bash
python3 tools/check.py --strict
python3 tools/roster.py --check
python3 -m unittest discover -s tools/tests -v
```

## Make a change

1. Branch from `main`. One topic per pull request, and do not stack pull
   requests on each other.
2. Add or edit the source, not the generated files. Regenerate generated files
   with the repository's generator instead of editing them by hand.
3. Run the checks:

   ```bash
   python3 tools/check.py --strict
   python3 tools/roster.py --check
   python3 -m unittest discover -s tools/tests -v
   ```

4. Open a pull request using the template. Include what changed, the exact
   commands and results, and any decision only the owner can make.
5. A reviewer that did not write the change checks it against the description.
   The owner approves the latest commit.

## What the rules require

- Do not push or force-push to `main`. Merge with a merge commit; the repository
  does not use squash or rebase merges.
- Every pull request needs a code owner's approval. The `*` catch-all in
  `.github/CODEOWNERS` covers every path, so every change is covered.
- A push after an approval makes that approval stale. Say so on the pull request
  before you push to an approved branch.
- Workflows set `permissions` and pin every action to a full commit SHA.
- Do not commit secrets, credentials, or personal absolute paths.

## Adding or importing a skill

Start with [docs/how-to/write-a-skill.md](docs/how-to/write-a-skill.md). An
imported skill needs `PROVENANCE.md` and an entry in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Adding a role

Role charters live in `roles/<role>/ROLE.md` and list the skills they use. A
new role must pass the admission test in [roles/README.md](roles/README.md).
Start with [docs/how-to/add-a-role.md](docs/how-to/add-a-role.md), then run
`python3 tools/roster.py` and `python3 tools/check.py --strict`.

## What happens next

CI runs `check.py --strict` and the unit tests on Python 3.13 and 3.14.
Dependabot keeps the pinned actions current. The `protect-main` ruleset requires
a code-owner review, resolved review threads, the `check` jobs, the CodeQL
checks, and an approval of the latest push. If any are missing, leave the merge
to the owner.

## Organization access

Every account in the `The-Urcydo` organization belongs to the owner.
`nguyenquocduyloc` and `NguyenLoc231` are the owner's accounts; `kusarine`,
`shiniroku`, `shinkir6u`, and `Shinkirou231` are agent-operated clones, not
independent maintainers. The current access model and its accepted risk are
recorded in [ADR 0008](docs/decisions/0008-single-owner-organization-access.md).
Agent accounts never approve a pull request or merge.

## Releasing

There is no release process yet. The version is `v0.1` in progress; tags and
release notes will be added when the first version is ready.

## Questions

Open an issue using the question form.
