# Roles

Role charters describe who is acting, what they read, which skills they use, and when they stop. They do not own the skills; the library in `../skills/` is shared.

A charter lives at `roles/<role>/ROLE.md`. The front matter is:

```yaml
---
role: reviewer
tier: flow
mission: Independently verify that finished work meets its acceptance criteria and the repository's rules.
reads: [AGENTS.md, "the work item", "the diff"]
skills: [write-skill]
never: [review work you built, fix the findings yourself]
done_when: The review has a verdict, per-criterion evidence, and ranked findings.
escalate_when: The acceptance criteria look wrong, or you find a security or data-loss problem.
---
```

- `role` must equal the folder name.
- `tier` is `flow`, `advisory`, or `optional`.
- `skills` lists skill names from `../skills/`; every name must exist.
- `reads` and `never` are lists.
- `done_when` is one observable condition; `escalate_when` is a list or a sentence.

Roles run as hats by default. A separate session is required only for independent review, and for security when that role is installed. The charters arrive in Batch 4; `ROSTER.md` will be generated from them.
