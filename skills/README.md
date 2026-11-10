# Skills

The library. One flat folder per skill.

```text
skills/
├── README.md
└── <name>/
    ├── SKILL.md
    ├── references/     # optional
    ├── scripts/        # optional
    ├── assets/         # optional
    └── PROVENANCE.md   # imported skills only
```

## Rules

- The folder name is the skill name and matches the `name` field.
- Names are unique, lowercase, and hyphenated.
- `SKILL.md` follows the [skill format](../docs/reference/skill-format.md).
- The source uses only open Agent Skills fields. Tool-specific behavior belongs in generated adapters.
- A skill never contains role logic. Role charters list the skills they use.
- Keep `SKILL.md` under 500 lines; put detail in `references/`.
- Imported skills need `PROVENANCE.md` and an entry in `THIRD_PARTY_NOTICES.md`.
- `SKILLS.md` at the repository root is generated from `metadata.category`; do not hand-edit it.

## Add a skill

```bash
mkdir -p skills/my-skill
# write skills/my-skill/SKILL.md
python3 tools/check.py
```

The scaffolding, catalog, and installation tools arrive in Batch 1. Until then, create the folder and `SKILL.md` by hand.

## Categories

`engineering`, `productivity`, `design`, `repo`. The category is metadata, not a folder. Adding a category changes the checker and the catalog; propose it in an ADR first.
