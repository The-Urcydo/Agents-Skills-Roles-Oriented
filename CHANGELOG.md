# Changelog

All notable changes to this repository are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Bootstrap the skills-first repository: folder shape, skill contract, checker, decisions, docs, and CI.
- Batch 1: `tools/new_skill.py`, `tools/catalog.py`, `tools/install.py`, generated `SKILLS.md`, the first skill (`write-skill`), and the installation guide.

### Security

- Enable secret scanning, push protection, Dependabot alerts and security updates, private vulnerability reporting, and CodeQL.
- Protect `main` with Code Owner review, required checks, merge-only commits, and a release-tag ruleset.
- Add `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue forms, and a governance ADR.
- Harden CI with concurrency, a timeout, manual dispatch, and tests for pinned actions and governance files.
