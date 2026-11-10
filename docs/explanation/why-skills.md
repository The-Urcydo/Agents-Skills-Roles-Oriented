# Why skills

An `AGENTS.md` file is always loaded. That is right for facts every session needs: commands, hard rules, where things are. It is the wrong place for a procedure used once a week. Every line in `AGENTS.md` costs context in every session, whether or not the task needs it.

A skill moves a procedure out of the always-loaded file and into a folder the agent opens only when the task calls for it.

## Progressive disclosure

1. **Metadata.** At startup the agent sees `name` and `description` for every available skill. That is roughly 100 tokens per skill, not the body.
2. **Instructions.** When the description matches the task, the agent loads `SKILL.md`. This is the procedure.
3. **Resources.** If the procedure points to `references/`, `scripts/`, or `assets/`, the agent loads or runs them only at that point.

The result: a library of detailed procedures without paying for all of them on every turn.

## Skills, roles, and AGENTS.md

| Layer | Question it answers | Loaded |
|---|---|---|
| `AGENTS.md` | What is always true here? | Every session |
| Role charter | Who is acting, what they own, when they stop? | When the agent takes that role |
| Skill | How do I do this task? | When the task matches |

A role charter says *when* a role uses a skill. A skill says *what* to do. Neither should duplicate the other.

## Roles consume skills

The reviewer charter, for example, lists `review-work` and `write-handoff`; the procedure for evidence, severity, and verdict lives in the skill. The planner uses `new-work-item`; the scribe uses `write-doc`. This keeps one copy of each procedure and lets a second role use it without duplicating the text. The generated [role roster](../../roles/ROSTER.md) shows which skills each role consumes.

The library ports the Repo-Template harness; [ADR 0007](../decisions/0007-port-the-agent-roles-and-skills.md) records what changed in the port and what stayed behind.

## Model-invoked vs user-invoked

Most skills are safe for the agent to start when the task matches. Some change shared state, spend money, or need the owner's explicit grant. Those are user-invoked: the agent must not start them on its own. In the source, record that as `metadata.invocation: user`; the adapter for each tool translates it into the tool's own control.

## Why this repository is skills-first

Repo-Template already provides the runnable scaffold: docs, work items, roles, protocols, and tools. What it lacks is a deep, validated library of procedures. This repository builds that library, keeps each skill portable, and gives role charters a clean list of skills to consume. The library can then be copied into Repo-Template without carrying a second scaffold with it.
