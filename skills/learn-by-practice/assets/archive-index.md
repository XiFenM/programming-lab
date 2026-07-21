# {{SUBJECT}} learning archive

This directory preserves both the final understanding and the path used to reach it: source-based
explanations, learner questions, practice artifacts, experiments, reviews, revisions, mastery
checks, pause checkpoints, and visible dialogue archives.

## Program profile

| Field | Value |
| --- | --- |
| Subject | {{SUBJECT_TABLE}} |
| Subject slug | `{{SUBJECT_SLUG}}` |
| Intended outcome | To be agreed with the learner |
| Primary sources | {{SOURCE_DESCRIPTION_TABLE}} |
| Started | {{START_DATE}} |
| Archive state | active |

## Learning loop

1. Orient the lesson and verify prerequisites.
2. Explain one complete source unit and its mental model.
3. Resolve and record learner questions.
4. Assign graduated practice with explicit acceptance criteria.
5. Let the learner create the artifact.
6. Review with numbered, evidence-backed findings.
7. Let the learner revise and verify each finding.
8. Check conceptual, practical, and transferable mastery.
9. Close or pause with a recovery checkpoint and post-hoc dialogue archive.

## Directory layout

```text
.
├── README.md
├── templates/lesson-record.md
├── lessons/
├── dialogues/
├── references/
└── attachments/
```

- Keep lesson conclusions in `lessons/` and generated visible dialogue in `dialogues/`.
- Keep practice artifacts in the repository's normal source locations and link to them.
- Keep bulky generated evidence in `attachments/<lesson>/`.
- Do not edit authoritative source snapshots merely to add notes.

## Lesson index

Use states: `not-started`, `explaining`, `questions`, `practicing`, `reviewing`,
`mastery-check`, `paused`, and `complete`.

| Lesson | Source unit | Structured record | State | Dialogue |
| --- | --- | --- | --- | --- |
| 01 | To be selected | `lessons/01-<lesson>.md` | not-started | not exported |

## Current checkpoint

| Field | Current value |
| --- | --- |
| Active lesson | Lesson 01, not started |
| Current phase | Course setup |
| Latest evidence | Archive initialized |
| Open work | Select the first source unit and confirm learning objectives |
| Next action | Create the first lesson from `templates/lesson-record.md` |
| Advancement gate | Lesson-specific blocking findings closed and mastery demonstrated |
| Dialogue | Not yet exported |

## Dialogue index

| Segment | Scope | File | Message count | Status |
| --- | --- | --- | --- | --- |
| — | — | — | — | not exported |

## Recording principles

- Separate source facts, observations, explanations, inferences, and learner understanding.
- Preserve mistakes, failed experiments, changed assumptions, and review history.
- Record reproducible evidence before claiming correctness or performance.
- Treat “changed,” “verified,” and “closed” as different review states.
- Keep structured conclusions separate from unedited visible dialogue.
- Resume from the latest checkpoint instead of reconstructing the course from memory.
