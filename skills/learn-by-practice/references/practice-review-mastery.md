# Practice, review, and mastery

Use this reference when designing exercises, reviewing learner artifacts, planning revisions,
or deciding whether a lesson can close.

## Contents

1. [Exercise ladder](#exercise-ladder)
2. [Exercise contract](#exercise-contract)
3. [Hint policy](#hint-policy)
4. [Review model](#review-model)
5. [Finding lifecycle](#finding-lifecycle)
6. [Mastery gate](#mastery-gate)

## Exercise ladder

Select the smallest ladder that exposes the target concept:

1. **Reproduction**: rebuild or re-derive the central mechanism without copying line by line.
2. **Boundary variation**: change size, shape, input class, assumption, or operating condition.
3. **Transfer**: apply the same model to a related but structurally different problem.
4. **Evaluation**: compare alternatives, explain tradeoffs, or predict behavior before testing.

Do not require every rung in every lesson. Always include enough variation to distinguish
understanding from memorization.

For non-code subjects, replace implementation with an observable artifact such as a proof,
worked example, critique, design, experiment, explanation, or decision memo.

## Exercise contract

Specify each exercise with:

| Field | Purpose |
| --- | --- |
| Learning objective | Name the exact concept being tested |
| Task | State the artifact the learner must produce |
| Must satisfy | Define observable functional or conceptual requirements |
| Constraints | Prevent bypassing the target concept |
| Representative cases | Cover normal, boundary, and invalid/counterexample behavior |
| Validation | Give commands, comparison method, rubric, or expected invariant |
| Allowed hints | Bound how much scaffolding is available initially |
| Completion definition | State what must be true before review begins |
| Optional extension | Offer deeper work that does not block the lesson |

Avoid hidden requirements. If an important requirement is discovered during review, label it
as a newly clarified contract item rather than blaming the learner for missing it.

## Hint policy

Use progressive hints:

1. Restate the invariant or ask a diagnostic question.
2. Point to the relevant source section or concept.
3. Show a smaller analogous example.
4. Suggest pseudocode, a test case, or a partial structure.
5. Provide the implementation only when the learner explicitly requests it or continued
   blocking would prevent the intended learning outcome.

Record material hints because they change what “independent completion” means at mastery time.

## Review model

Inspect the submitted artifact and its contract before forming conclusions. Reproduce behavior
with project-native checks where practical. Review in this order:

1. Contract correctness and conceptual fidelity.
2. Boundary, invalid-input, and failure behavior.
3. Test or evidence quality and reproducibility.
4. Clarity, maintainability, and consistency with repository conventions.
5. Performance, efficiency, or elegance when required by the lesson.

Use severities consistently:

| Severity | Meaning |
| --- | --- |
| `blocking` | Incorrect result, invalid model, unsafe behavior, or missing core requirement |
| `major` | Important boundary, evidence, robustness, or design gap |
| `minor` | Quality issue worth fixing but not a mastery blocker by itself |
| `suggestion` | Optional improvement or alternative worth considering |
| `question` | Clarification needed before judging the implementation |

Lead the review with findings. For each finding record:

- durable ID, severity, and status;
- exact artifact location or behavior;
- evidence or reproduction;
- why it matters to the lesson objective;
- a repair direction without taking over the exercise;
- the learner's response and later verification.

## Finding lifecycle

Use these states:

```text
open -> learner-revised -> verified -> closed
  |           |
  |           -> needs-more-work
  -> rejected-with-rationale
  -> deferred-with-owner-and-gate
```

“Code changed” is not “verified.” Close a finding only after checking the relevant behavior or
after documenting a justified rejection. Keep earlier review rounds and their outcomes.

If the user asks Codex to implement fixes, separate review findings from implementation work and
report which findings were changed and verified. Do not silently collapse the learning loop into
an agent-authored solution.

## Mastery gate

Require evidence in three dimensions:

### Conceptual

- Restate the central model without copying the lesson explanation.
- Explain one boundary, counterexample, or failure mode.
- Predict what changes when a key assumption changes.

### Practical

- Produce the required artifact independently enough for the lesson's goal.
- Pass required correctness or rubric checks.
- Complete at least one meaningful variation or transfer task.

### Reflective

- Identify an earlier misconception, failed attempt, or design tradeoff.
- Explain why the final approach works and what remains uncertain.

Close the lesson only when all blocking findings are closed, required evidence is reproducible,
the transfer check passes, the archive is synchronized, and the learner agrees to advance.
Optional performance work or explicitly deferred minor issues may remain if the record states why
they do not block mastery.
