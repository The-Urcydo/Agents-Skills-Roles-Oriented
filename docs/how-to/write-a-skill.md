# Write a skill

Use this when a procedure is repeated across sessions and does not belong in the always-loaded `AGENTS.md`.

## 1. Decide that it is a skill

A skill is a procedure: steps, checks, and stop conditions. A fact ("the test command is X") belongs in `AGENTS.md`. A role's ownership ("the reviewer never fixes findings") belongs in a role charter. If the content is a one-off, it belongs in the pull request.

The split is in [the skill format](../reference/skill-format.md#charter-skill-or-document): a charter holds routing and limits, a skill holds the procedure, and a fact about the repository belongs in `docs/`.

Routing that changes who owns a work item or what its status is belongs in a role charter or a protocol, not a skill. A skill may point to that rule; it must not restate it. If a skill only restates its charter, it is not worth adding.

## 2. Pick the name

- Lowercase letters, digits, and single hyphens.
- The folder name and the `name` field must match.
- The name must be unique across the flat library.
- Prefer a verb or a short noun phrase: `code-review`, `write-handoff`, `diagnosing-bugs`.

## 3. Create the folder

```bash
python3 tools/new_skill.py my-skill --category engineering
```

This creates `skills/my-skill/SKILL.md` and updates `SKILLS.md`. To do it by hand, `mkdir -p skills/my-skill`, write the file, then run `python3 tools/catalog.py`.

Add `references/`, `scripts/`, or `assets/` only if the skill needs them.

## 4. Write the front matter

```yaml
---
name: my-skill
description: Does a specific job. Use when the user asks for that job or the task matches these triggers.
license: MIT
metadata:
  category: engineering
  invocation: both
---
```

`category` is one of `engineering`, `productivity`, `design`, or `repo`. `invocation` is `model`, `user`, or `both`. See [the skill format](../reference/skill-format.md) for every rule.

## 5. Write the body

1. State what the skill does and when it applies.
2. Give the steps in order.
3. State how to verify the result.
4. List edge cases and when to stop and ask.
5. Keep it under 500 lines; move the long tail into `references/`.

Do not put role names in the skill. If a role should use it, add the skill name to that role's charter. Do not put routing that changes a work item's owner or status in the skill; that belongs in the charter or protocol.

## 6. Add resources

- `references/`: detailed rules, examples, checklists. Link them from `SKILL.md` with relative paths, one level deep.
- `scripts/`: executable helpers. State the runtime, dependencies, network needs, and failure behavior.
- `assets/`: templates, images, or data the skill copies or reads.

## 7. Imported skills

If the skill comes from another repository, add `PROVENANCE.md` with the source URL, exact commit or tag, author, license, changes, and import date. Add the entry to `THIRD_PARTY_NOTICES.md`. Do not vendor a large asset pack without an explicit decision.

## 8. Validate

```bash
python3 tools/check.py --strict
```

Fix every error. Warnings do not fail the default check, but CI uses `--strict`. The checker also fails when `SKILLS.md` is out of date; run `python3 tools/catalog.py` after adding or editing a skill. A fresh scaffold contains `TODO` markers; replace them, because `--strict` warns on any remaining placeholder.

## 9. Open the pull request

Include:

- the skill name and the trigger;
- the check output;
- one example of the skill working, or a clear reason it cannot be exercised yet;
- for imports, the provenance file and the license.

A quick installation test:

```bash
mkdir -p /tmp/skill-test
python3 tools/install.py --target claude --skill my-skill --project /tmp/skill-test
```

## Checklist

- [ ] Name matches the folder and is unique.
- [ ] Description says what the skill does and when to use it.
- [ ] License is present.
- [ ] `metadata.category` is valid.
- [ ] No role logic and no tool-specific front matter.
- [ ] No TODO placeholders remain.
- [ ] Links resolve from the skill folder root; body is under 500 lines.
- [ ] `SKILLS.md` is up to date.
- [ ] Imported skill has `PROVENANCE.md`.
- [ ] `python3 tools/check.py --strict` passes.
