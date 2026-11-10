# Skill format

This is the contract every skill in `skills/` follows. It is the open Agent Skills format plus two repository metadata keys.

## Folder

```text
skills/<name>/
├── SKILL.md          # required
├── references/       # optional: detail loaded on demand
├── scripts/          # optional: executable helpers
├── assets/           # optional: templates, images, data
└── PROVENANCE.md     # required for imported skills
```

The folder name is the skill name. It is flat under `skills/`; there are no category folders.

## Front matter

```yaml
---
name: code-review
description: Review a diff along two axes and report findings. Use when asked to review a branch, PR, or work in progress.
license: MIT
compatibility: Requires git and a shell.
metadata:
  category: engineering
  invocation: both
allowed-tools: Read Grep Bash(git:*)
---
```

### Required

| Field | Rule |
|---|---|
| `name` | 1-64 chars; lowercase letters, digits, single hyphens; must equal the folder name. |
| `description` | 1-1024 chars; says what the skill does **and when to use it**. |
| `license` | Required by this repository (the open spec makes it optional). Use `MIT` for original skills; use the upstream license for imports. |

### Optional

| Field | Rule |
|---|---|
| `compatibility` | 1-500 chars; environment requirements only. |
| `metadata` | String map. This repo uses `category` and `invocation`. |
| `allowed-tools` | Space-separated pre-approved tools. Experimental; document the need. |

### Repository metadata

| Key | Values | Meaning |
|---|---|---|
| `metadata.category` | `engineering`, `productivity`, `design`, `repo` | The catalog group. Required. |
| `metadata.invocation` | `model`, `user`, `both` | Who may start the skill. Default `both`. `user` means the agent must not start it on its own; adapters map it to the tool's control. |

Do **not** put role names in a skill. Role charters list the skills they use. Do not use Claude-only fields (`disable-model-invocation`, `argument-hint`, `hooks`, `context`) in the source; adapters add them.

## Body

- Start with what the skill does and when it applies.
- Write steps an agent can follow without guessing.
- State the verification: the command, check, or observable result.
- List edge cases and stop conditions.
- Keep `SKILL.md` under 500 lines. Move detail into `references/`.
- Keep file references one level deep from `SKILL.md`.
- No secrets, credentials, personal paths, or machine-specific assumptions.

## Progressive disclosure

The agent sees `name` and `description` at startup. It loads the body only when the skill matches the task. It loads `references/`, runs `scripts/`, or reads `assets/` only when the body points to them. Put the common path in `SKILL.md`; put the long tail in `references/`.

## Validation

```bash
python3 tools/check.py
```

The checker validates names, front matter, license, metadata, links, and the 500-line limit. `--strict` makes warnings fail. It also fails when `SKILLS.md` does not match the skill folders.

```bash
python3 tools/catalog.py --check
```

If the reference validator is available, `skills-ref validate skills/<name>` should also pass.

## Quality checklist

- [ ] The description names both the job and the trigger.
- [ ] The body has a clear first step and a verification step.
- [ ] Every relative link resolves.
- [ ] No role logic and no tool-specific front matter.
- [ ] An imported skill has `PROVENANCE.md`.
- [ ] `python3 tools/check.py` passes.
