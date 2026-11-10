---
name: review-security
description: "Review a change for security and privacy risk and report findings by severity with a recommended fix. Use when a change touches authentication, data, dependencies, infrastructure, or anything exposed to users."
license: MIT
compatibility: "Requires access to the change and the repository's threat model."
metadata:
  category: engineering
  invocation: both
---
# Review security

Use this for changes that add inputs, trust boundaries, secrets, dependencies, permissions, or user-facing surface. It is a focused review, not a substitute for the repository's tests.

## Steps

1. Read the change and the brief. Map what it adds or changes: inputs, data flows, trust boundaries, secrets, dependencies, permissions, and error paths.
2. Compare the change with the threat model in the repository. If the change adds surface the model does not cover, update the model or recommend the update.
3. Look for the common failures:
   - untrusted input reaching a shell, query, path, or template;
   - secrets in code, logs, fixtures, or error messages;
   - missing authorization, not just missing authentication;
   - unsafe defaults, permissive CORS, or broad tokens;
   - dependencies with known vulnerabilities or unexpected install scripts;
   - personal data collected, logged, or retained without a reason.
4. Write each finding with impact, evidence, and a recommended fix. Rank it `blocker` (must fix before approval), `major` (must fix or the human accepts), or `minor` (fix now or log it).
5. If a finding needs the human (risk acceptance, disclosure, spend), ask with a recommendation and the cost of guessing wrong.
6. Report; do not fix. Hand the review back through the tracker.

## Verify

- The review names the change and the surfaces it adds.
- Every finding has impact, evidence, and a fix.
- Secrets are described by location, not value.
- The threat model is current, or the update is listed.
- The human owns any accepted risk.

## In Repo-Template

- Write `security-review.md` with `python3 tools/item_file.py <id> security-review`.
- The threat model lives in `docs/security/`.
- Hand back through `python3 tools/transition.py`; do not fix the findings.

## Stop and ask

- You find an exposed secret, a data-loss risk, or a privacy issue.
- A finding needs disclosure or risk acceptance.
- The change needs production access or spend to verify.
- You cannot tell whether the behavior is intended; ask instead of assuming.
