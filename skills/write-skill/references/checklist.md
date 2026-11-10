# Skill checklist

In this library, the canonical contract is `docs/reference/skill-format.md` at the repository root. When this skill is installed in another project, this checklist is the standalone contract.

## Front matter

| Field | Rule |
|---|---|
| `name` | String, 1-64 chars; lowercase letters, digits, single hyphens; equals the folder name. |
| `description` | String, 1-1024 chars; what it does and when to use it. |
| `license` | String; `MIT` for original work; upstream license for imports. |
| `metadata.category` | `engineering`, `productivity`, `design`, or `repo`. |
| `metadata.invocation` | `model`, `user`, or `both`. Use `user` for shared state, spend, or owner approval. |
| `compatibility` | Optional string; 1-500 chars; environment requirements only. |
| `allowed-tools` | Optional string; space-separated; no commas. |

Only the fields in this table are allowed. Claude-only fields (for example `disable-model-invocation`, `argument-hint`, `hooks`, `context`, `paths`) are rejected.

## Body

- [ ] Opens with what the skill does and when it applies.
- [ ] Steps are ordered and concrete.
- [ ] Verification is a command, check, or observable result.
- [ ] Stop conditions are explicit.
- [ ] Under 500 lines; detail is in `references/`.
- [ ] No TODO placeholders remain.
- [ ] Relative links resolve from the skill folder root.
- [ ] No secrets, personal paths, or machine-specific assumptions.
- [ ] No role names; role charters list the skills they use.

## Validation

- In this library: `python3 tools/catalog.py --check` and `python3 tools/check.py --strict`.
- Elsewhere: `skills-ref validate <skill-folder>` if available. `skills-ref` is a separate Python package; installing it may need network access. Otherwise, use this checklist.

## Imported skills

- [ ] `PROVENANCE.md` has source URL, commit, author, license, changes, and date.
- [ ] `THIRD_PARTY_NOTICES.md` has the roll-up entry.
- [ ] The upstream license is compatible with MIT distribution.
