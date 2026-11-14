# Port to Repo-Template

This guide moves a validated skill or harness change from this library into [Repo-Template](https://github.com/The-Urcydo/Repo-Template). It is not a sync and not a copy of the whole repository: Repo-Template owns the runnable scaffold, this repository owns the skill library.

Read [ADR 0007](../decisions/0007-port-the-agent-roles-and-skills.md) and [ADR 0009](../decisions/0009-split-role-routing-from-skill-method.md) first. On the Repo-Template side, read `template/agents/AGENTS.md`, `template/docs/dev/how-to/add-a-skill.md`, `template/docs/dev/how-to/add-a-role.md`, and `template/docs/dev/reference/front-matter.md`.

## What are you porting?

| Change here | Where it goes in Repo-Template |
|---|---|
| A skill several roles use | `template/agents/skills/<name>/` |
| A skill only one role uses | `template/agents/roles/<role>/skills/<name>/` |
| A role charter change | `template/agents/roles/<role>/ROLE.md` |
| A protocol change | `template/agents/protocols/<name>.md` |
| A doc | `template/docs/dev/` (or the audience folder it belongs to) with front matter |
| A new decision | `template/docs/decisions/NNNN-title.md` |

Repo-Template has two skill lanes because a role can be cut as a module. This repository has one flat lane because a skill is role-agnostic. Choose the lane again when you port; do not copy the flat layout into Repo-Template.

## Port a skill

1. **Choose the lane.** Use `template/agents/skills/<name>/` when several roles or any agent can use the skill. Use `template/agents/roles/<role>/skills/<name>/` when only one role uses it. The name must be unique across both lanes because `.claude/skills/` is flat.
2. **Copy the folder.** Copy `skills/<name>/` and keep `references/`, `scripts/`, and `assets/` with it.
3. **Convert the front matter.** Keep `name` and `description`. Map this repository's metadata to Repo-Template's fields:

   | Here | In Repo-Template |
   |---|---|
   | `name`, `description` | keep unchanged |
   | `license` | keep; the open spec allows it and Repo-Template's checker ignores extra fields |
   | `metadata.invocation: user` | `disable-model-invocation: true` |
   | `metadata.invocation: model` or `both` | remove the key |
   | `metadata.category` | remove it, or keep it as a note; Repo-Template has no catalog group |
   | `compatibility`, `allowed-tools` | keep if the skill needs them; Repo-Template's checker ignores them |

4. **Remove role logic.** There must be no `**Role:**` line, no role name, and no command that moves a work item. The method stays in `SKILL.md`; the role's `ROLE.md` points to the skill. If the skill needs a routing rule, put the rule in the charter and have the skill point to it.
5. **Replace tracker language.** A generic step such as "hand the item to the reviewer" becomes the exact command:

   ```bash
   python3 tools/transition.py <id> --owner reviewer --next "Reviewer: read security-review.md, then finish review.md"
   ```

   Use `python3 tools/item_file.py <id> <file>` for an item artifact and `python3 tools/check.py --strict` for the final check.
6. **Add the pointer.** In the role's `ROLE.md`, add the skill to the step that uses it, or to a `Procedure` line. Do not copy the steps into the charter.
7. **Keep the role lane non-empty.** A role folder needs `skills/`; if it has no skill, keep `skills/.gitkeep`. Delete the `.gitkeep` when the first skill arrives.
8. **Regenerate and verify:**

   ```bash
   python3 tools/sync_agents.py
   python3 tools/check.py --strict
   ```

## Port a role charter

1. **Start from the Repo-Template `ROLE.md`.** Do not overwrite it with this repository's fields. Map the fields:

   | Here | In Repo-Template |
   |---|---|
   | `role`, `mission`, `reads`, `never`, `done_when`, `escalate_when` | keep |
   | `tier` | remove; Repo-Template has no tier field |
   | `skills` | remove; the adapter reads the role's `skills/` folder, not a field |
   | `access` | keep; `read-only` maps to the adapter's `disallowedTools` |
   | `use_when` | keep; it completes the generated description |
   | — | add `item_files` for the item files this role exclusively writes |
   | — | add `writes_files` for root files this role exclusively writes |

2. **Move role-only skills.** If a skill in this charter's `skills` list is used only by this role, put it under `roles/<role>/skills/`. Shared skills stay in `agents/skills/`.
3. **Keep ownership exclusive.** Two roles must not claim the same `item_files` or `writes_files` entry. Repo-Template's checker fails on the duplicate.
4. **Update the lifecycle.** If the role joins the flow, update the dispatch table in `agents/README.md`, `DEFAULT_OWNER` in `tools/_lib.py`, and the rules in `agents/protocols/handoff.md` together.
5. **Add an eval when the role is new.** Repo-Template's `agents/evals/` has golden tasks; add one that exercises the role's routing.
6. **Regenerate and verify:**

   ```bash
   python3 tools/sync_agents.py
   python3 tools/check.py --strict
   python3 -m unittest discover -s tools/tests
   ```

## Port a protocol

1. Keep the rule, replace the generic language with Repo-Template's paths and commands.
2. The reference state machine in `agents/protocols/handoff.md` matches Repo-Template's states. Use `work/items/<id>/handoff.md` for a full item and `work/items/<id>.md` for a light item.
3. Every status change goes through `python3 tools/transition.py`, with `--by`, `--next`, and `--evidence` where the state requires it.
4. Keep the `Docs for the scribe:` line exact. The reviewer routes on it; `transition.py` does not read it.
5. The security route is enforced by `transition.py`: `verified` is refused when the brief says `required` and `security-review.md` is missing.
6. Add or update an eval task when the protocol changes routing. `security-routing` and `conditional-scribe` are the models.

## Port a doc

Repo-Template docs use front matter. Add it:

```yaml
---
title: Title
type: tutorial | how-to | reference | explanation | decision | index | meta
status: placeholder | draft | active | deprecated | generated
summary: One sentence, at most 240 characters.
owner_role: architect
---
```

Use the Diataxis type that matches the reader's need. Run `python3 tools/sync_indexes.py` instead of hand-editing `docs/INDEX.md`. Do not link from core docs into optional module folders; use backticks.

## Verification

In Repo-Template:

```bash
python3 tools/check.py --strict
python3 tools/sync_agents.py --check
python3 -m unittest discover -s tools/tests
python -m pytest tests -q        # the template's own tests, when you changed template/
```

If the evals module is installed:

```bash
python3 tools/eval_harness.py --list
python3 tools/eval_harness.py --verify-fixtures
python3 tools/eval_harness.py --cmd "your-agent-cli --role {role} --prompt {prompt}"
```

Record the real-agent run in `agents/evals/results/README.md`.

## Do not port

- This repository's `tools/` (`catalog.py`, `roster.py`, `install.py`, `new_skill.py`). Repo-Template has its own tools.
- `SKILLS.md` or `roles/ROSTER.md`. Both are generated in Repo-Template too.
- The flat layout as a reason to flatten Repo-Template's role bundles. Role-local skills make a role cuttable; keep that property.
- This repository's `AGENTS.md`. Repo-Template's generated root comes from `template/AGENTS.md.jinja`.
- `docs/` front matter rules from this repository. Repo-Template requires front matter; this repository does not.
- A new ADR number without checking Repo-Template's `docs/decisions/` and open pull requests first.

## Checklist

- [ ] The skill lane is correct: shared or role-local.
- [ ] `metadata.invocation: user` became `disable-model-invocation: true`.
- [ ] No role name and no routing command is left in the skill.
- [ ] The role `ROLE.md` points to the skill; it does not copy the steps.
- [ ] `tier` and `skills` were removed or mapped; `access` and `use_when` were kept.
- [ ] A lifecycle role updates the dispatch table, `DEFAULT_OWNER`, and the handoff protocol.
- [ ] Protocols use `work/` and `tools/` commands, not generic tracker language.
- [ ] Docs have front matter and the index was regenerated.
- [ ] `check.py --strict`, the sync check, and the unit tests pass.
- [ ] The golden tasks pass, or the reason they were not run is recorded.
- [ ] The owner approved the harness change before merge.
