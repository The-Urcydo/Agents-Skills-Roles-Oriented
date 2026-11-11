---
title: Keep the single-owner organization access model
status: accepted
date: 2026-11-11
summary: Every organization account belongs to the owner; keep the admin default and no 2FA requirement, and record the accepted residual risk.
---

# 0008: Keep the single-owner organization access model

## Context

[ADR 0006](0006-repository-governance.md) recorded a gap: every member of the
`The-Urcydo` organization had organization and repository admin, the default
repository permission was `admin`, and the organization did not require
two-factor authentication. That record assumed the organization had human
owners plus separate agent-operated accounts.

That assumption does not match this organization. Every account is the owner's:
`nguyenquocduyloc` and `NguyenLoc231` are the owner's accounts, and `kusarine`,
`shiniroku`, `shinkir6u`, and `Shinkirou231` are agent-operated clones. There is
one human, not a group of independent maintainers.

## Decision

- Keep the current access model. The owner's accounts and clones hold
  organization and repository admin, and the organization default repository
  permission stays `admin`.
- Do not require two-factor authentication for the organization now. The owner
  accepts the risk for these accounts.
- Agent-operated accounts never approve a pull request and never merge. The
  `protect-main` ruleset, the `*` catch-all in `.github/CODEOWNERS`, the required
  checks, and the no-bypass rule are the review controls.
- If the organization ever gains an independent human member, revisit this
  decision before granting access: set the default repository permission to
  `none`, require 2FA, and give agent identities write access only. Prefer a
  GitHub App over a user account for unattended agents.

## Consequences

- The review boundary is not a hard boundary. An organization admin can change
  the ruleset or the security settings. This is accepted because the only admins
  are the owner's own accounts.
- A compromised agent account has the same access as the owner. Treat agent
  credentials as owner credentials.
- A future second human must not inherit the `admin` default or the 2FA
  exemption.

## Verification

```bash
gh api orgs/The-Urcydo --jq '{default_repository_permission,two_factor_requirement_enabled}'
gh api "orgs/The-Urcydo/members?role=admin" --jq '.[].login'
gh api "orgs/The-Urcydo/members?filter=2fa_disabled" --jq '.[].login'
gh api repos/The-Urcydo/Agents-Skills-Roles-Oriented/collaborators \
  --jq '.[] | [.login,.role_name] | @tsv'
```

Expected current state: default `admin`, 2FA `false`, every admin is one of the
owner's accounts or a clone, and the repository admins are the owner's accounts
or clones. The four agent clones appear in the 2FA-disabled list; that is
accepted.

## Related

- [ADR 0006](0006-repository-governance.md): the original governance decision
  and the gap this record accepts.
- [CONTRIBUTING.md](../../CONTRIBUTING.md): the contributor-facing summary.
