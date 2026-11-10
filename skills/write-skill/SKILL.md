---
name: write-skill
description: "Create or revise a skill in this repository. Use when adding a skill, fixing an existing skill, or asked how to write one."
license: MIT
metadata:
  category: repo
  invocation: both
---
# Write a skill

Use this when a procedure should become a skill. A skill is a procedure, not a fact and not a role rule.

1. Confirm the content is a skill. Facts every session needs go in `AGENTS.md`. Role ownership and stop conditions go in `roles/<role>/ROLE.md`. A one-off change belongs in the pull request.
2. Read `references/checklist.md` for the front matter and quality rules.
3. Scaffold the folder:
   ```
   python3 tools/new_skill.py <name> --category <engineering|productivity|design|repo>
   ```
4. Write the description first. It must say what the skill does and when to use it; that is the only text the agent sees before loading the body.
5. Write the body: what the skill does, ordered steps, how to verify the result, and when to stop and ask.
6. Add `references/`, `scripts/`, or `assets/` only when the body needs them. Keep links inside the skill folder so the skill stays portable.
7. If the skill is imported, add `PROVENANCE.md` and update `THIRD_PARTY_NOTICES.md`.
8. Validate:
   ```
   python3 tools/check.py --strict
   ```
9. Open a pull request with the skill name, the trigger, and the check output.

## Stop and ask

- The request is a fact, a role rule, or a one-off.
- The skill would need a secret, a personal path, or undocumented network access.
- An existing skill already covers the job: improve that skill instead of adding a near-duplicate.
- The skill changes shared state or spends money: mark it `metadata.invocation: user` and get the owner's approval.
