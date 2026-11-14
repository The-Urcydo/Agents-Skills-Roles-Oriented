# Why skills

An `AGENTS.md` file is always loaded. That is right for facts every session needs: commands, hard rules, where things are. It is the wrong place for a procedure used once a week. Every line in `AGENTS.md` costs context in every session, whether or not the task needs it.

A skill moves a procedure out of the always-loaded file and into a folder the agent opens only when the task calls for it.

## Progressive disclosure

1. **Metadata.** At startup the agent sees `name` and `description` for every available skill. That is roughly 100 tokens per skill, not the body.
2. **Instructions.** When the description matches the task, the agent loads `SKILL.md`. This is the procedure.
3. **Resources.** If the procedure points to `references/`, `scripts/`, or `assets/`, the agent loads or runs them only at that point.

The result: a library of detailed procedures without paying for all of them on every turn.

## Context budget

The design follows a three-tier loading rule:

1. **Always loaded.** The root `AGENTS.md` is short on purpose: commands, hard rules, and where things are. Every line costs context in every session.
2. **Indexes.** `docs/INDEX.md`, `SKILLS.md`, `roles/ROSTER.md`, and `agents/README.md` say what exists without opening it. Read the index, then open only the page the task needs.
3. **Content.** Docs, role charters, protocols, references, and skill bodies are opened only when the task matches.

A skill's metadata is the cheap tier: the agent sees `name` and `description` at startup and loads the body only when the task matches. A role charter is read when the agent takes that role, so it holds the rules that must never be skipped. The procedure moves to a skill, where it costs almost nothing until it is needed.

Repo-Template's `docs/dev/explanation/context-budget.md` summarizes the research behind this rule. The practical conclusion is restraint: keep the always-loaded file short, put detail in the next tier, and test the harness rather than assuming it helps.

## Skills, roles, and AGENTS.md

| Layer | Question it answers | Loaded |
|---|---|---|
| `AGENTS.md` | What is always true here? | Every session |
| Role charter | Who is acting, what they own, when they stop? | When the agent takes that role |
| Skill | How do I do this task? | When the task matches |

A role charter says *when* a role uses a skill. A skill says *what* to do. Neither should duplicate the other.

The charter also holds routing: every rule that changes who owns an item or what its status is. The skill holds the method: read order, checks, templates, and commands that do not move the item. A fact lives in one place; if both need it, the charter states the rule and the skill points to it. [ADR 0009](../decisions/0009-split-role-routing-from-skill-method.md) records the split; [the role format](../reference/role-format.md) gives the fields.

## Roles consume skills

The reviewer charter, for example, lists `review-work` and `write-handoff`; the procedure for evidence, severity, and verdict lives in the skill. The planner uses `new-work-item`; the scribe uses `write-doc`. This keeps one copy of each procedure and lets a second role use it without duplicating the text. The generated [role roster](../../roles/ROSTER.md) shows which skills each role consumes.

The library ports the Repo-Template harness; [ADR 0007](../decisions/0007-port-the-agent-roles-and-skills.md) records what changed in the port and what stayed behind.

## Model-invoked vs user-invoked

Most skills are safe for the agent to start when the task matches. Some change shared state, spend money, or need the owner's explicit grant. Those are user-invoked: the agent must not start them on its own. In the source, record that as `metadata.invocation: user`; the adapter for each tool translates it into the tool's own control.

## Why this repository is skills-first

Repo-Template already provides the runnable scaffold: docs, work items, roles, protocols, and tools. What it lacks is a deep, validated library of procedures. This repository builds that library, keeps each skill portable, and gives role charters a clean list of skills to consume. The library can then be copied into Repo-Template without carrying a second scaffold with it.
