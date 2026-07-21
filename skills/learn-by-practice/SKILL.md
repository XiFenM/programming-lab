---
name: learn-by-practice
description: Run structured, repository-aware learning programs that combine source-based explanation, learner questions, graduated practice, artifact review, revision, mastery checks, durable progress records, and post-hoc dialogue archives. Use when a user asks Codex to teach or study a technical or non-technical topic over multiple sessions; learn from tutorials, documentation, examples, papers, or a codebase; assign and review exercises; resume a paused course; maintain a learning journal; or transfer this guided-learning workflow to another subject or repository.
---

# Learn by Practice

Build understanding through a repeatable loop: explain, question, practice, review,
revise, demonstrate mastery, and preserve the evidence. Keep the learner in control of
the practice work and treat the archive as part of the learning process.

## Choose the operating mode

Infer the narrowest mode that satisfies the request:

- **Start a course**: inspect sources, agree on scope and outcomes, create an archive,
  and begin the first lesson.
- **Continue a lesson**: recover the current checkpoint and resume the next unfinished
  phase without repeating completed material.
- **Resolve questions**: answer the learner's questions, test the explanation with a
  minimal example when useful, and update the lesson record.
- **Assign practice**: design exercises that target the concepts just discussed and
  define observable acceptance criteria.
- **Review work**: inspect the learner's artifact, run proportionate checks, record
  findings, and let the learner revise unless they explicitly ask for implementation.
- **Pause or close**: write a recovery checkpoint, synchronize evidence, and export the
  visible dialogue when the session source is available.

Do not force a full course archive for a one-off explanation unless the user asks for
ongoing study or durable records.

## Establish or recover context

1. Inspect repository instructions, layout, current status, relevant source material,
   existing learning records, and available validation commands.
2. Infer the topic, learner level, source authority, desired outcome, and artifact
   location when evidence is strong. Ask one concise question only when a missing choice
   would materially change the course.
3. Prefer primary material selected by the user. Distinguish source behavior, observed
   results, explanations, and hypotheses in both teaching and records.
4. When an archive already exists, read its index, the active lesson, and the latest
   pause checkpoint before acting. Preserve its conventions and history.
5. When durable records are requested and no archive exists, read
   [references/learning-archive.md](references/learning-archive.md), then run
   `scripts/init_learning_archive.py`. Adapt to an established repository convention
   instead of creating a competing documentation tree.

## Run one learning cycle at a time

### 1. Orient the lesson

- Identify the exact source unit, prerequisites, learning objectives, and completion
  evidence.
- Map the source's structure and execution or argument flow before discussing details.
- Record uncertain prerequisites without turning them into assumed deficiencies.

### 2. Explain the complete case

- Explain motivation, vocabulary, components, data or control flow, constraints,
  boundary behavior, verification, and tradeoffs at the learner's level.
- Tie explanations to exact local files or authoritative sources.
- Use small examples, diagrams, or experiments only when they materially clarify a
  relationship.
- Finish with the mental model the learner should be able to restate, then invite
  questions before assigning practice.

### 3. Resolve questions

- Preserve each original question and the learner's initial assumption.
- Answer the mechanism behind the behavior, not only the immediate symptom.
- Separate closely related operations when conflating them would create a fragile
  mental model.
- Confirm the resolved conclusion and record any derived question.

### 4. Design graduated practice

- Target recently discussed concepts rather than introducing unrelated complexity.
- Provide purpose, task, constraints, allowed hints, representative cases, validation
  method, completion definition, and optional extensions.
- Include at least one boundary or counterexample and one transfer variation when the
  subject permits it.
- Keep the core implementation for the learner. Supply scaffolding or stronger hints
  only when requested or when the learner is genuinely blocked.

### 5. Review the learner's artifact

- Inspect before editing. Run repository-native validation in proportion to the risk.
- Lead with correctness and conceptual fidelity; then cover boundaries, error behavior,
  clarity, maintainability, reproducibility, and performance where relevant.
- Number findings, assign a severity, cite evidence, propose a direction, and track the
  learner's disposition across revisions.
- Distinguish “implemented” from “verified” and “closed.” Do not erase failed attempts
  or superseded findings from the record.

### 6. Verify mastery

- Ask the learner to restate the central model in their own words.
- Require an independent variation, prediction, comparison, or application that cannot
  be completed by copying the source mechanically.
- Close the lesson only when blocking findings are closed, required evidence passes,
  the explanation is transferable, and the learner agrees to proceed.

Read [references/practice-review-mastery.md](references/practice-review-mastery.md) when
designing nontrivial exercises, reviewing an artifact, or deciding whether a lesson is
complete.

## Keep records synchronized

Update the structured lesson record at meaningful transitions: after the main
explanation, after each question cluster, when assigning practice, after every review,
after verification, and at pause or completion. Link to source and learner artifacts;
do not duplicate large implementations that will drift.

Preserve:

- misunderstandings and their corrections;
- failed experiments, hypotheses, commands, and observed output;
- numbered review findings and their state transitions;
- environment details needed to reproduce results;
- the current checkpoint and exact next actions.

Keep structured conclusions separate from raw dialogue. Never rewrite a raw dialogue
archive to make the learning process appear cleaner.

## Pause, resume, and archive dialogue

When interrupted, add a checkpoint containing the current phase, completed work,
evidence, open findings, unresolved questions, next ordered actions, and the gate for
advancing. On resume, use that checkpoint as the entry point.

At a lesson boundary or deliberate pause, read
[references/dialogue-archive.md](references/dialogue-archive.md) and use
`scripts/export_codex_dialogue.py` when the Codex rollout JSONL is accessible. Select
explicit start and end boundaries, review privacy and message counts, and link the
generated archive from the structured lesson. Treat an active-session export as a
versioned snapshot that may need regeneration when the lesson finally closes.

## Resource map

- `scripts/init_learning_archive.py`: create a new subject archive without overwriting
  existing material.
- `scripts/export_codex_dialogue.py`: extract user-visible dialogue from one Codex
  rollout JSONL with provenance and safe boundary selection.
- `assets/archive-index.md`: template consumed by the archive initializer.
- `assets/lesson-record.md`: comprehensive, domain-neutral lesson template.
- [references/learning-archive.md](references/learning-archive.md): archive layout,
  lifecycle, update rules, and migration guidance.
- [references/practice-review-mastery.md](references/practice-review-mastery.md):
  exercise design, review taxonomy, and mastery gates.
- [references/dialogue-archive.md](references/dialogue-archive.md): post-hoc extraction,
  privacy review, and multi-session handling.
