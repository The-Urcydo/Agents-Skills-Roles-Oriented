# Finding severity

| Severity | Meaning | Effect |
|---|---|---|
| blocker | Wrong, unsafe, breaks a rule or an accepted decision | Must fix before approval |
| major | Meets the letter but misses the intent, or is fragile | Must fix or be accepted by the human |
| minor | Style, naming, or a small improvement | Fix now or log a new item |

A finding states:

- **What:** the defect in one sentence.
- **Where:** file and line, or the exact command.
- **Why:** the impact if it ships.
- **Fix:** the smallest change that resolves it.

Do not inflate a style preference into a blocker. Do not soften a data-loss risk into a minor.
