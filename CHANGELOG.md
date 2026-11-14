# Changelog

All notable changes to this repository are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Bootstrap the skills-first repository: folder shape, skill contract, checker, decisions, docs, and CI.
- Batch 1: `tools/new_skill.py`, `tools/catalog.py`, `tools/install.py`, generated `SKILLS.md`, the first skill (`write-skill`), and the installation guide.
- Batch 4: port the Repo-Template agent harness: eight role charters, eight skills (`new-work-item`, `write-handoff`, `merge-work`, `write-doc`, `review-work`, `record-decision`, `research-question`, `review-security`), five protocols, and the generated `roles/ROSTER.md`.
- Add `tools/roster.py`, role front matter and skill-name validation in `check.py`, and tests for both.
- Batch 5: add optional `access` and `use_when` role fields with checker validation, [the role format](docs/reference/role-format.md), [the harness rules](agents/AGENTS.md), and [the porting guide](docs/how-to/port-to-repo-template.md).
- Add [ADR 0009](docs/decisions/0009-split-role-routing-from-skill-method.md), recording the Repo-Template charter/method port and its deliberate exclusions.

### Changed

- The `agents/` harness now has protocols in place; adapters and evals remain documented placeholders.
- Role charters now hold routing and limits while skills hold the method. The reviewer routes a required security review before any verdict and routes on the builder's `Docs for the scribe:` line; the builder writes that line; the scribe skips a confirmed `none`; the orchestrator closes it.
- Update the protocols with the reference handoff state machine, the security and docs routing, and the post-merge record. Add nested rules for `agents/`.
- `AGENTS.md` and `CONTRIBUTING.md` include the roster check.
- Move CI from Python 3.9 to Python 3.13 and 3.14, and pin the runner to `ubuntu-24.04`.
- Simplify `.github/CODEOWNERS` to one `*` catch-all line and remove the redundant test that policed the duplicate lines.
- Check links in every root `*.md` document from `tools/check.py` instead of a separate governance test.

### Security

- Enable secret scanning, push protection, Dependabot alerts and security updates, private vulnerability reporting, and CodeQL.
- Require the CodeQL and `Analyze` checks on `main`.
- Record the single-owner, multi-machine organization access model and require 2FA in [ADR 0008](docs/decisions/0008-single-owner-organization-access.md).
- Protect `main` with Code Owner review, required checks, merge-only commits, and a release-tag ruleset.
- Add `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue forms, and a governance ADR.
- Harden CI with concurrency, a timeout, manual dispatch, and tests for pinned actions and governance files.
