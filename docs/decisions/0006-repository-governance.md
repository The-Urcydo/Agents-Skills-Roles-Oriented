---
title: Protect main and report security privately
status: accepted
date: 2026-11-10
summary: Use a GitHub ruleset, Code Owner review, pinned CI, Dependabot, and private vulnerability reporting; only human owners keep admin.
---

# 0006: Protect main and report security privately

## Context

This is a public library of agent instructions and standard-library Python
tools. Agents contribute in pull requests, and the human owner decides. A
mistake in a skill can reach an agent that runs it, so the repository needs a
review boundary, a private way to report a vulnerability, and a CI pipeline that
does not trust mutable tags.

The repository already had a `protect-main` ruleset, a CODEOWNERS file, and a
CI workflow with SHA-pinned actions. It had no security policy, no Dependabot
configuration, and no enforcement of the workflow pinning rule.

## Decision

- `main` is protected by the `protect-main` ruleset: a pull request, one Code
  Owner review, dismissal of stale reviews, approval of the latest push, the
  `check` jobs, no bypass actors, and merge commits only.
- `.github/CODEOWNERS` has a catch-all line for the human owners. Agent-operated
  accounts must never approve or hold admin.
- Security reports go through GitHub's private vulnerability reporting, as
  described in [SECURITY.md](../../SECURITY.md). Do not open a public issue with
  the details.
- Secret scanning, push protection, Dependabot alerts, Dependabot security
  updates, and private vulnerability reporting are enabled.
- Workflows use a read-only default token, set `permissions`, and pin every
  action to a full commit SHA. Dependabot keeps the pins current.
- The repository uses merge commits. Squash and rebase merges are disabled.

## Consequences

- Every change lands through a pull request. Direct pushes and force-pushes to
  `main` are blocked.
- A new third-party action needs an explicit allow decision and a pinned SHA.
- A push after an approval makes that approval stale; the owner reviews the
  latest commit.
- Security reports stay private until a fix is ready.
- The repository is public, so secret scanning and code scanning are available
  without a paid plan.

## Known gap

Every member of the `The-Urcydo` organization currently has organization admin
and repository admin access, including the agent-operated accounts. An
organization admin can change the ruleset or the security settings, so the
review boundary is not a hard boundary until the organization access model is
fixed. The intended state is that only human owners hold admin, and agent
accounts get the least privilege they need on this repository. That change is
tracked separately because it affects other repositories in the organization.
