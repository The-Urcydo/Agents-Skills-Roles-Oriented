# GitHub merge gate

Use this when the forge is GitHub. The repository's settings are the real gate; these are the checks to look for.

## What to confirm

- The default branch has a ruleset or branch protection: pull request required, at least one approving review, stale approvals dismissed, the required checks green, and merge commits allowed. If any of these are missing, say so once in the handoff; the procedure still applies, but the gate is weaker.
- The pull request's head commit is the one CI ran on. A push after the approval makes the approval stale.
- CODEOWNERS review is satisfied for the paths the branch changes.
- The merge method is a merge commit; squash and rebase are disabled or not used.
- The branch is not behind the base in a way that changes the result; update it and wait for CI again.

## Commands

```bash
gh pr view <number> --json state,mergeable,reviewDecision,statusCheckRollup,headRefOid
gh pr checks <number>
gh pr merge <number> --merge
```

`gh pr merge --merge` uses a merge commit. Do not pass `--squash` or `--rebase`. If the repository requires a different method, follow the repository's rule.

## Stop

- A required check is missing or red on the head commit.
- The approval is stale, or a code owner has not reviewed a path they own.
- The pull request changes files the owner did not approve.
- The merge would delete or rewrite history.
