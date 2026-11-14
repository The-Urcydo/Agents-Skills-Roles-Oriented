# Plan template

Copy the parts the host does not already provide. Keep the plan next to the work item or link it from the handoff.

## Plan

```markdown
# Plan: <title>

## Goal

<The outcome in one or two sentences, copied from the brief.>

## Acceptance criteria

- [ ] <Observable criterion from the brief.>

## Approach

<How the work will be done, in a few sentences. Name the files or components involved.>

## Risks and unknowns

| Risk or unknown | Likelihood | Mitigation | What would make the plan wrong |
|---|---|---|---|
| <...> | low / medium / high | <...> | <...> |

## Sequencing

<What must happen first, what can run in parallel, and what must wait for a merge.>

## How it will be tested

<The commands, checks, observable behavior, and evidence the verifier will need.>

## Out of scope

<What this plan deliberately does not do.>
```

## Tasks

```markdown
# Tasks: <title>

- [ ] 1. <First concrete step, small enough for one session.>
- [ ] 2. <Next step.>
- [ ] 3. <Tests for the change.>
- [ ] 4. <Run the repository check and the project tests.>
- [ ] 5. <Write the handoff and the docs decision.>
```

## Handoff line

When the plan is ready, give the agent doing the work one sentence: the first task and the plan's path. If a decision is still open, name the question and leave that task out of the plan until it is answered.
