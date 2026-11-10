## Summary

<!-- One topic, one short paragraph: what changed and why. -->

## Evidence

<!-- Commands and exact results. Include `python3 tools/check.py` and, when tools/ changed, the unit tests. -->

## Security impact

<!-- None, or what changed and why it is safe. Mention settings, workflows, secrets, or permissions. -->

## Merge danger

**Door:** <!-- one-way or two-way -->

**Blast radius:** <!-- layout, consumers, tooling, etc. -->

## Checklist

- [ ] I did not commit secrets, credentials, or personal absolute paths.
- [ ] Workflow changes set `permissions` and pin actions to full commit SHAs.
- [ ] I ran `python3 tools/check.py --strict` and the unit tests.
- [ ] Generated files were regenerated, not hand-edited.
