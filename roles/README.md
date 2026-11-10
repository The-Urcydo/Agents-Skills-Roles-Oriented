# Roles

Role charters describe who is acting, what they read, which skills they use, and when they stop. They do not own the skills; the library in `../skills/` is shared.

The generated [role roster](ROSTER.md) lists every role, its tier, and the skills it uses. `python3 tools/roster.py` regenerates it; `python3 tools/roster.py --check` verifies it. Do not hand-edit the roster.

## Charter

A charter lives at `roles/<role>/ROLE.md`. The front matter is:

```yaml
---
role: reviewer
tier: flow
mission: Independently verify that finished work meets its acceptance criteria and the repository's rules.
reads: [AGENTS.md, "the work item", "the diff"]
skills: [review-work, write-handoff]
never: [review work you built, fix the findings yourself]
done_when: The review has a verdict, per-criterion evidence, and ranked findings.
escalate_when: The acceptance criteria look wrong, or you find a security or data-loss problem.
---
```

Only these fields are allowed:

| Field | Rule |
|---|---|
| `role` | Must equal the folder name. |
| `tier` | `flow`, `advisory`, or `optional`. |
| `mission` | One sentence: what the role is for. |
| `reads` | Non-empty list of paths or short descriptions. |
| `skills` | List of skill names from `../skills/`; every name must exist. Empty is allowed but unusual. |
| `never` | Non-empty list of things the role must not do. |
| `done_when` | One observable condition. |
| `escalate_when` | One sentence or a list: when the role stops and asks. |

The charter body says how the role runs and points at its skills. The procedure belongs in `SKILL.md`; the charter does not duplicate it.

## Tiers and modes

- **flow**: works inside the host's work loop (orchestrator, planner, builder, reviewer, scribe).
- **advisory**: produces an artifact on request (architect, researcher).
- **optional**: installed only when the project needs it (security).

Roles run as hats by default: the session holding the item reads the charter and acts as that role. A separate session is required for review, and preferred for security. The researcher is callable: the caller keeps the item.

## Add a role

1. Check the admission test: exclusive ownership, a different access level, the checker half of a maker/checker pair, or enough work to need its own context window. Otherwise write a skill instead.
2. Create `roles/<name>/ROLE.md` with the front matter above.
3. List the skills it uses. Do not copy a skill's procedure into the charter.
4. Run `python3 tools/roster.py` and `python3 tools/check.py --strict`.
5. Open a pull request with the role, the skills, and the check output.
