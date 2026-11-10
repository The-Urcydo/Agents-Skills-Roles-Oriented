---
title: Adopt a skills-first library
status: accepted
date: 2026-11-10
summary: Build this repository as a portable skill library, not as a second Copier template.
---

# 0001: Adopt a skills-first library

## Context

Repo-Template is a Copier template: it generates a runnable project skeleton with docs, work items, roles, protocols, and tools. The new repository exists to develop agent skills and later move them into Repo-Template. Maintaining a second Copier template would duplicate the scaffold and split maintenance.

## Decision

This repository is a portable library. Its primary product is `skills/`, with `roles/` as consumers and `agents/` as the harness around them. It does not generate projects and does not carry a `work/` state machine.

## Consequences

- Skills can be installed into any existing repository, including Repo-Template.
- The repository stays focused on the skill contract and the library.
- Porting into Repo-Template needs an explicit mapping, documented in the porting guide.
- If a generated project becomes necessary later, a thin wrapper can be added without changing the skill source.
