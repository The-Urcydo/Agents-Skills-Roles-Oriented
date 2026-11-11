---
title: Keep the single-owner, multi-machine organization access model
status: accepted
date: 2026-11-12
summary: Four owner accounts on separate home machines keep organization admin; 2FA is required; the owner accepts the shared-trust model.
---

# 0008: Keep the single-owner, multi-machine organization access model

Status: accepted. The owner approved this decision when approving the plan for
PR #4; the pull-request approval will confirm it.

## Context

[ADR 0006](0006-repository-governance.md) recorded a gap: every member of the
`The-Urcydo` organization had organization and repository admin, the default
repository permission was `admin`, and the organization did not require
two-factor authentication. That record assumed human owners plus separate
agent-operated accounts.

That assumption does not match this organization. The owner has four accounts,
one per home machine: `nguyenquocduyloc`, `NguyenLoc231`, `shiniroku`, and
`shinkir6u`. Every account belongs to the same human. The owner drives agent
sessions from those machines, but the accounts are not independent maintainers.
`kusarine` and `Shinkirou231` were unused and have been removed.

The per-machine accounts keep the organization owner role because those machines
need to create and add repositories and work across the organization. A member
role would require extra per-repository grants and break that workflow. The owner
accepts the broader permission that comes with the role.

## Decision

- Keep the current access model. The owner's four accounts hold organization and
  repository admin, and the organization default repository permission stays
  `admin`.
- Require two-factor authentication for the organization. All four accounts
  already have it, so the requirement removes nobody; it prevents a future
  account or collaborator from skipping 2FA.
- Accounts used to drive unattended agent sessions never approve a pull request
  and never merge. The `protect-main` ruleset, the `*` catch-all in
  `.github/CODEOWNERS`, the required checks, and the no-bypass rule are the
  review controls.
- If the organization ever gains an independent human member, revisit this
  decision before granting access: set the default repository permission to
  `none`, keep 2FA required, and give agent identities write access only. Prefer
  a GitHub App over a user account for unattended agents.

## Consequences

- The review boundary is not a hard boundary. An organization admin can change
  the ruleset or the security settings. This is accepted because every admin is
  one of the owner's accounts.
- A compromised machine account has the same access as the owner. Treat every
  account's credentials as owner credentials.
- The owner role is broader than the minimum needed to create and work on
  repositories. The owner accepts that tradeoff for the multi-machine workflow.
- A future second human must not inherit the `admin` default or the owner role
  without a new decision.

## Verification

```bash
gh api orgs/The-Urcydo --jq '{default_repository_permission,two_factor_requirement_enabled}'
gh api "orgs/The-Urcydo/members?role=admin" --jq '.[].login'
gh api "orgs/The-Urcydo/members?filter=2fa_disabled" --jq '.[].login'
gh api repos/The-Urcydo/Agents-Skills-Roles-Oriented/collaborators \
  --jq '.[] | [.login,.role_name] | @tsv'
```

Expected current state: default `admin`, 2FA `true`, the admins are the owner's
four accounts, the 2FA-disabled list is empty, and the repository admins are the
owner's accounts.

## Related

- [ADR 0006](0006-repository-governance.md): the original governance decision
  and the gap this record accepts.
- [CONTRIBUTING.md](../../CONTRIBUTING.md): the contributor-facing summary.
