# Security policy

## Supported versions

Only the latest commit on `main` is supported. This repository is a library of
instructions and standard-library Python tools, not a released package; fixes
land on `main`.

## Reporting a vulnerability

Please report security problems privately. Do not open a public issue with the
details.

Use GitHub's private vulnerability reporting: open the **Security** tab of this
repository and choose **Report a vulnerability**.

Include:

- what is affected: `tools/`, a `SKILL.md`, a script under `skills/*/scripts/`,
  a workflow, or a repository setting;
- the steps to reproduce, or the smallest proof;
- the impact you believe it has;
- any suggested fix or mitigation.

We will acknowledge the report as soon as we can and keep you informed. This is
a small project, so there is no fixed response time.

## What is in scope

- The Python tools under `tools/`, including path handling, file writes, and the
  installer's target handling.
- Executable helpers under `skills/*/scripts/`.
- The workflows and repository settings this repository relies on.
- A skill whose instructions are likely to make an agent leak data, run
  destructive commands, or bypass the owner's approval.

## What is out of scope

- The behavior of a third-party agent, model, or tool that loads a skill.
- Vulnerabilities in a project that installed a skill, unless the skill itself
  caused them.
- Vulnerabilities in an upstream project or action; report those upstream.
- Content that is clearly a test fixture or an example and cannot affect a real
  agent.

## Organization access

The `The-Urcydo` organization is a single-owner setup. Every account belongs to
the owner; the non-owner accounts are agent-operated clones. Treat a compromised
agent account as a compromised owner account. See
[ADR 0008](docs/decisions/0008-single-owner-organization-access.md) for the
access model and its residual risk.

## Safe use

- Never commit credentials, tokens, or private keys. Secret scanning and push
  protection are enabled.
- Treat a skill as code you run with your agent: read it before installing it.
- Imported skills carry a `PROVENANCE.md`. Report a missing or misleading
  provenance as a security problem.
