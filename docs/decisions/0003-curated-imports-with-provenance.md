---
title: Curate third-party skills with provenance
status: accepted
date: 2026-11-10
summary: Import third-party skills only after adaptation, with source, commit, license, and changes recorded.
---

# 0003: Curate third-party skills with provenance

## Context

The library draws on widely used MIT skills from Matt Pocock and others, plus installed skills such as `grilling`, `pr`, and `find-skills`. Upstream skills often assume their author's repository conventions. Copying them as-is would import hidden dependencies and unclear ownership.

## Decision

Curate and adapt. Every imported skill has a `PROVENANCE.md` recording the source URL, exact commit or tag, author, license, changes, and import date. `THIRD_PARTY_NOTICES.md` rolls the entries up. The full `taste-skill` bundle is not imported in v0.1; a lightweight design skill may be written later.

## Consequences

- Imported behavior is understood and tested in this repository's context.
- License and attribution are explicit.
- Adaptation takes longer than copying.
- Upstream updates are manual; the provenance file says what to compare.
