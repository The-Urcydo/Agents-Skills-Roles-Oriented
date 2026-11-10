# Skill checklist

## Front matter

| Field | Rule |
|---|---|
| `name` | 1-64 chars; lowercase letters, digits, single hyphens; equals the folder name. |
| `description` | 1-1024 chars; what it does and when to use it. |
| `license` | `MIT` for original work; upstream license for imports. |
| `metadata.category` | `engineering`, `productivity`, `design`, or `repo`. |
| `metadata.invocation` | `model`, `user`, or `both`. Use `user` for shared-state or spend. |
| `compatibility` | Optional; environment requirements only. |
| `allowed-tools` | Optional; space-separated. |

Do not use Claude-only fields in the source: `disable-model-invocation`, `argument-hint`, `hooks`, `context`, `paths`.

## Body

- [ ] Opens with what the skill does and when it applies.
- [ ] Steps are ordered and concrete.
- [ ] Verification is a command, check, or observable result.
- [ ] Stop conditions are explicit.
- [ ] Under 500 lines; detail is in `references/`.
- [ ] Relative links stay inside the skill folder.
- [ ] No secrets, personal paths, or machine-specific assumptions.
- [ ] No role names; role charters list the skills they use.

## Imported skills

- [ ] `PROVENANCE.md` has source URL, commit, author, license, changes, and date.
- [ ] `THIRD_PARTY_NOTICES.md` has the roll-up entry.
- [ ] The upstream license is compatible with MIT distribution.
