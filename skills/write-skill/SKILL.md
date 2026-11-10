---
name: write-skill
description: "Create or revise an agent skill in this library or a project's agent skills directory. Use when adding a skill, fixing an existing skill, or asked how to write one."
license: MIT
metadata:
  category: repo
  invocation: both
---
# Write a skill

Use this when a procedure should become a skill. A skill is a procedure, not a fact and not a role rule.

When working in this library, the commands use Python 3.9+ and the standard library only; they need no network access.

1. Confirm the content is a skill. Facts every session needs go in `AGENTS.md`. Role ownership and stop conditions go in `roles/<role>/ROLE.md`. A one-off change belongs in the pull request.
2. Read [references/checklist.md](references/checklist.md) for the front matter and quality rules.
3. Create the folder:
   - In this library: `python3 tools/new_skill.py <name> --category <engineering|productivity|design|repo>`. This creates `skills/<name>/SKILL.md` and updates `SKILLS.md`. If you create it by hand, run `python3 tools/catalog.py` after editing.
   - In another project: create `<name>/SKILL.md` inside that project's agent skills directory, for example `.agents/skills/<name>/SKILL.md` (portable), `.claude/skills/<name>/SKILL.md`, or `.opencode/skills/<name>/SKILL.md`.
4. Write the description first. It must say what the skill does and when to use it; that is the only text the agent sees before loading the body.
5. Write the body: what the skill does, ordered steps, how to verify the result, and when to stop and ask.
6. Add `references/`, `scripts/`, or `assets/` only when the body needs them. Keep links inside the skill folder, relative to the skill folder root, so the skill stays portable.
7. If the skill is imported, add `PROVENANCE.md` and update `THIRD_PARTY_NOTICES.md` when the host repository has one.
8. Validate with the commands under [Verify](#verify).
9. In this library, open a pull request with the skill name, the trigger, and the check output. In another project, follow that project's review process. Do not merge it; the owner approves.

## Verify

- In this library: `python3 tools/catalog.py --check` and `python3 tools/check.py --strict` pass.
- Elsewhere: `skills-ref validate <skill-folder>` passes if it is installed. `skills-ref` is a separate Python package; installing it may need network access. If it is unavailable, satisfy every item in [references/checklist.md](references/checklist.md).

## Stop and ask

- The request is a fact, a role rule, or a one-off.
- The skill would need a secret, a personal path, or undocumented network access.
- An existing skill already covers the job: improve that skill instead of adding a near-duplicate.
- The skill you are writing changes shared state or spends money: mark that skill `metadata.invocation: user` and get the owner's approval.
