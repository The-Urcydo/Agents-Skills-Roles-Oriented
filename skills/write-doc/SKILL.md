---
name: write-doc
description: "Create or update a documentation page in the repository's docs system, using the right Diataxis type and a one-sentence summary. Use whenever adding, changing, moving, or deleting documentation."
license: MIT
compatibility: "Works with any Markdown docs folder; the commands below assume the repository has a docs index."
metadata:
  category: productivity
  invocation: both
---
# Write a doc

Use this when a change makes documentation wrong or incomplete, or when a reader needs a page that does not exist. Pick one Diataxis type per page; if a page needs two types, write two pages and link them.

## Steps

1. Pick the type by the reader's need:
   - **Tutorial:** a beginner learns by doing; the steps work every time.
   - **How-to:** someone who knows the basics solves one task; a recipe.
   - **Reference:** someone looks up a fact; accurate, complete, no opinions or instructions.
   - **Explanation:** someone wants to understand why; context, trade-offs, history.
2. Check the docs index first. Update an existing page instead of adding a near-duplicate.
3. Write the page:
   - start with the reader's problem and the outcome;
   - keep one job per page;
   - use the repository's front matter and summary field;
   - link related pages and code;
   - state the last verification date when the page describes code.
4. Delete or mark deprecated anything the change makes wrong. A stale page is worse than no page.
5. Regenerate the docs index with the repository's tool, not by hand.
6. Verify every command and link on the page; run the repository's docs check.

## Verify

- The page has one type and one job.
- The index lists it with a one-sentence summary.
- Every command, path, and link resolves.
- No page the change made wrong is left active.
- The docs check passes.

## In Repo-Template

```bash
python3 tools/new_doc.py <tutorial|how-to|reference|explanation> "Title" --summary "One sentence a stranger can judge by."
python3 tools/sync_indexes.py
python3 tools/check.py
```

Docs live under `docs/`; the generated index is `docs/INDEX.md`. Do not link from core docs into optional module folders; use backticks.

## Stop and ask

- The page needs two types; split it instead of guessing.
- The fact is unverified or the code and docs disagree.
- The change would delete a page another team owns.
- The page would contain a secret or a personal path.
