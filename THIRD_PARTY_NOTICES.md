# Third-party notices

This repository contains original skills, first-party ports from another repository owned by the same owner, and, when marked, skills adapted from third-party sources. Each imported skill keeps its upstream license and copyright. The canonical record is the skill's `PROVENANCE.md`; this file is the roll-up.

No third-party skills have been imported yet.

## First-party ports

These skills come from another repository owned by the same owner. Each has a `PROVENANCE.md`; [ADR 0007](docs/decisions/0007-port-the-agent-roles-and-skills.md) records the decision.

| Skill | Source | Commit | License |
|---|---|---|---|
| `new-work-item` | Repo-Template `template/agents/skills/new-work-item/SKILL.md` | `c0ab1a8` | MIT |
| `write-handoff` | Repo-Template `template/agents/skills/write-handoff/SKILL.md` | `c0ab1a8` | MIT |
| `merge-work` | Repo-Template `template/agents/skills/merge-work/` | `c0ab1a8` | MIT |
| `write-doc` | Repo-Template `template/agents/skills/write-doc/SKILL.md` | `c0ab1a8` | MIT |
| `review-work` | Repo-Template `template/agents/roles/reviewer/ROLE.md` and `template/agents/protocols/review.md` | `c0ab1a8` | MIT |
| `record-decision` | Repo-Template `template/agents/roles/architect/ROLE.md` and `template/docs/dev/how-to/write-an-adr.md` | `c0ab1a8` | MIT |
| `research-question` | Repo-Template `template/agents/roles/researcher/ROLE.md` | `c0ab1a8` | MIT |
| `review-security` | Repo-Template `template/agents/roles/security/ROLE.md` | `c0ab1a8` | MIT |
| `plan-work` | Repo-Template `template/agents/roles/planner/ROLE.md` and `template/work/_templates/plan.md`, `tasks.md`, `brief.md` | `a9233bf` | MIT |

## Entry format

When a skill is imported or adapted, add one entry:

| Skill | Source | Commit | License | Changes |
|---|---|---|---|---|
| `example-skill` | https://github.com/owner/repo | `<sha>` | MIT | Rewrote repo-specific paths; trimmed unused assets |

Also add `skills/<name>/PROVENANCE.md` with:

- source URL and the exact commit or tag;
- upstream author and copyright line;
- license name and a copy of the license or a link to it;
- what changed in this repo;
- the date of the import.
