# Role format

This is the contract for a role charter in `roles/<role>/ROLE.md`. A charter says who acts, what the role owns, and when it stops. The procedure for one task lives in a skill, not in the charter.

## Folder and name

```text
roles/<role>/
└── ROLE.md
```

The folder name is the role name. It is lowercase and hyphenated if it has more than one word, and the `role` field must equal it. The roster at `roles/ROSTER.md` is generated from these files.

## Front matter

```yaml
---
role: reviewer
tier: flow
mission: Independently verify that finished work meets its acceptance criteria and the repository's rules.
reads: [AGENTS.md, SKILLS.md, "the work item", "the diff under review"]
skills: [review-work, write-handoff]
never: [review work you built, edit the work under review, approve without running the checks yourself]
done_when: The review has a verdict, per-criterion evidence, and findings ranked by severity.
escalate_when: The acceptance criteria look wrong, or you find a security or data-loss problem.
access: read-only
---
```

### Required

| Field | Rule |
|---|---|
| `role` | String; must equal the folder name. |
| `tier` | `flow`, `advisory`, or `optional`. |
| `mission` | One sentence: what the role is for. |
| `reads` | Non-empty list of paths or short descriptions. |
| `skills` | List of skill names from `skills/`; every name must exist. Empty is allowed but unusual. |
| `never` | Non-empty list of things the role must not do. |
| `done_when` | One observable condition. |
| `escalate_when` | One sentence or a list: when the role stops and asks. |

### Optional

| Field | Rule |
|---|---|
| `access` | `full` (the default when the key is absent) or `read-only`. |
| `use_when` | A short phrase that completes "Use when ...". Set it for a role that is called and does not own the flow; leave it out for a role that is handed items. |

`access: read-only` is a tool-neutral hint, not a security boundary. It means the role researches or reviews but does not edit the work under review; it may still write its own artifact, such as a review note, and the files it owns, such as the threat model. The `never` list is the binding rule. A future adapter may turn `access` into a tool limit; until then, nothing enforces it mechanically.

`use_when` is for callable roles such as the researcher and the architect. A role that is handed a work item does not need it: its trigger is the item's owner.

## Body

The body says how the role runs and what it owns. It does not repeat a skill's steps.

- **How it runs:** hat, separate session, callable, or optional install.
- **What you own:** the artifact or decision the role is accountable for.
- **Skills you use:** a pointer to each skill, not a copy of its procedure.
- **Quality bar:** what a good result looks like; every charter has one.

A fact lives in one place. Routing, ownership, and stop rules belong in the charter; read order, checks, templates, and commands that do not move a work item belong in a skill. If both need a fact, the charter states the rule and the skill points to it.

## Charter or skill?

The split is in [the skill format](skill-format.md#charter-skill-or-document): a charter holds routing and limits, a skill holds the procedure, and a fact about the repository belongs in `docs/`. A role that is mostly routing needs no skill; a role that produces an artifact and has a method of its own gets one. A skill that only restates its charter is not added.

## Validation

```bash
python3 tools/roster.py
python3 tools/check.py --strict
```

The checker validates the required fields, the role name, the tier, every skill name, `access`, and `use_when`. It also fails when `roles/ROSTER.md` is out of date.

## Quality checklist

- [ ] The role passes the admission test in [roles/README.md](../../roles/README.md).
- [ ] The folder name equals `role`.
- [ ] Every skill in `skills` exists.
- [ ] The body does not duplicate a skill's procedure.
- [ ] `access` and `use_when` are present only when they add meaning.
- [ ] `python3 tools/check.py --strict` passes.
