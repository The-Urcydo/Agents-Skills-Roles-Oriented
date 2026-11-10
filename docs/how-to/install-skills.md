# Install skills

`tools/install.py` copies a skill folder into a project's agent skills directory. It copies the whole folder, including `references/`, `scripts/`, `assets/`, and `PROVENANCE.md`.

## Targets

| Target | Destination | Read by |
|---|---|---|
| `claude` | `.claude/skills/<name>/` | Claude Code; OpenCode compatibility |
| `opencode` | `.opencode/skills/<name>/` | OpenCode |
| `agents` | `.agents/skills/<name>/` | OpenCode compatibility, Skills CLI convention |

## Examples

Install one skill into a project:

```bash
python3 tools/install.py --target claude --skill write-skill --project ../my-app
```

Install every skill into OpenCode's own folder:

```bash
python3 tools/install.py --target opencode --all --project ../my-app
```

Preview without writing:

```bash
python3 tools/install.py --target agents --skill write-skill --project ../my-app --dry-run
```

Replace an existing copy:

```bash
python3 tools/install.py --target claude --skill write-skill --project ../my-app --force
```

## Verify

1. Confirm the folder exists: `ls ../my-app/.claude/skills/write-skill`.
2. Restart the agent so it reloads skills.
3. Ask for the trigger, or invoke it directly: `/write-skill` in Claude Code, `@write-skill` in OpenCode.

## Skills CLI

The flat `skills/` layout is discovered by the Skills CLI. From this repository:

```bash
npx skills add . --list
npx skills add . --skill write-skill -y
```

From another project, use the repository URL instead of `.`.

## Notes

- The installer copies; it does not symlink. Re-run it after changing a skill, or use `--force`.
- `tools/check.py` validates the source library, not the installed copy.
- The local installer remains the supported path in v0.1; the Skills CLI is a convenience.
- There is no uninstall command yet; delete the installed folder.
