# Add a role

Use this when a new role should exist, not when a procedure is missing. A missing procedure is a skill; a missing owner is a role.

## 1. Pass the admission test

A new role needs at least one of:

- exclusive ownership of paths or artifacts that no other role owns;
- a different access level from its callers;
- the checker half of a maker/checker pair;
- work output large enough to need its own context window.

If none apply, write a skill and add it to an existing charter. The roster and the charters are described in [roles/README.md](../../roles/README.md).

## 2. Create the charter

Create `roles/<name>/ROLE.md` with the front matter from [roles/README.md](../../roles/README.md):

```yaml
---
role: <name>
tier: flow
mission: One sentence.
reads: [AGENTS.md, "the work item"]
skills: [<skill-name>]
never: [something the role must not do]
done_when: One observable condition.
escalate_when: When the role stops and asks.
---
```

- `role` equals the folder name.
- `tier` is `flow`, `advisory`, or `optional`.
- `skills` lists existing names from the shared `skills/` library.
- The body says how the role runs and points at its skills. Do not copy the procedure into the charter.

## 3. Generate and validate

```bash
python3 tools/roster.py
python3 tools/check.py --strict
python3 -m unittest discover -s tools/tests -v
```

The roster is generated; do not edit it by hand. `check.py` fails when a charter names a missing skill, uses an unknown field or tier, or does not match its folder.

## 4. Open the pull request

Include the role, the skills it uses, the check output, and any decision that needs the owner. The role list is a harness change, so it needs the owner's approval.

## Checklist

- [ ] The role passes the admission test.
- [ ] `role` matches the folder.
- [ ] Every skill in `skills` exists.
- [ ] The charter body does not duplicate a skill.
- [ ] `roles/ROSTER.md` is regenerated.
- [ ] `python3 tools/check.py --strict` passes.
