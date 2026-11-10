---
title: Flat skills layout with a generated catalog
status: accepted
date: 2026-11-10
summary: Skills live in flat skills/<name>/ folders; category is metadata and SKILLS.md is generated.
---

# 0005: Flat skills layout with a generated catalog

## Context

Matt Pocock's repository groups skills under category folders. That is browsable, but porting into Repo-Template's flat `agents/skills/` lane would need a flattening step, and `npx skills` discovery is simplest with a flat `skills/` tree.

## Decision

Every skill is `skills/<name>/SKILL.md`. `metadata.category` is one of `engineering`, `productivity`, `design`, or `repo`. `tools/catalog.py` generates `SKILLS.md` grouped by category. Names are unique across the flat library.

## Consequences

- Copying a skill into Repo-Template is one folder copy.
- The folder tree has no category navigation; the generated catalog provides it.
- Names must be unique across all categories.
- Adding a category is a deliberate change to the checker and catalog, recorded in an ADR.
