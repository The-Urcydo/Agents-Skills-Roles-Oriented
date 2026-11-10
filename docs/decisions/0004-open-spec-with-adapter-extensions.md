---
title: Open spec first, adapter extensions
status: accepted
date: 2026-11-10
summary: Skill sources use the open Agent Skills fields; tool-specific behavior is generated into adapters.
---

# 0004: Open spec first, adapter extensions

## Context

Claude Code adds frontmatter fields such as `disable-model-invocation`, `argument-hint`, and `hooks`. The open Agent Skills spec defines `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. The library must work in Claude Code and OpenCode, and later in other agents.

## Decision

A `SKILL.md` source uses only the open spec fields. Repository metadata (`category`, `invocation`) lives under `metadata`. A generator maps those values to tool-specific files, such as Claude's `disable-model-invocation: true` for `metadata.invocation: user`.

## Consequences

- The same skill folder is portable across agents.
- Tool-specific behavior is isolated in generated adapters.
- Claude-only features cannot be used directly in the source; they need an adapter mapping.
- The checker enforces the source contract.
