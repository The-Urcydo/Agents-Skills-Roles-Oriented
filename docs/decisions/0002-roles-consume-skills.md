---
title: Roles consume skills
status: accepted
date: 2026-11-10
summary: Role charters list the skills they use; skills remain role-agnostic.
---

# 0002: Roles consume skills

## Context

Repo-Template groups a role with the skills only that role uses. That keeps a role bundle cuttable, but it ties a procedure to one harness. This repository needs skills that several roles, or any agent, can use.

## Decision

Skills live in the flat `skills/` library and never contain role logic. Role charters live in `roles/<role>/ROLE.md` and list the skill names they use.

## Consequences

- A skill can be used by several roles without duplication.
- A role charter is the only place that says when a role uses a skill.
- Porting to Repo-Template maps root skills into `agents/skills/` and role charters into role bundles.
- A skill that truly belongs to one role stays in the shared library in v0.1; role-exclusive lanes are out of scope.
