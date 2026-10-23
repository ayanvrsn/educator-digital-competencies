# Development of Web Application for Enhancing Digital Competencies of School Educators

Individual diploma project by **Ayan Abilbek**, SE-2401, Software Engineering, Astana IT University. Supervisor: **Aliya Katyetova**.

The application is intended to help school educators move from an initial assessment to short learning modules, practical work and visible progress. The three initial topics are digital resource creation, online assessment and responsible resource management. The expected outcome is an implemented and evaluated prototype; improved learning has not yet been demonstrated.

## Current status

23 October 2026: analysis/design review draft and a local HTML prototype. No production application, teacher interviews, learning outcomes or substantive supervisor review are claimed. The signed/forwarded Justification is preserved privately outside this repository. Its final scope is the basis for the proposal.

All implementation and documentation responsibilities belong to Ayan. The supervisor reviews scope, competence mapping and evaluation. Committee access is a project-review permission and does not authorise access to participant records.

## Scope and technology

Teacher/admin accounts, an initial assessment, three modules, practical submissions, rule-based recommendations and progress. Proposed implementation stack: Next.js, React, TypeScript, PostgreSQL. No AI tutor, school-record integration or formal competence certification is in scope. The present prototype uses plain HTML/CSS/JavaScript solely to make the design reviewable.

## Materials

- [Consolidated report](docs/First_Submission_Report.pdf)
- [Editable report](docs/report.html)
- [Architecture diagrams and editable SVG sources](diagrams/)
- [Interactive UX prototype](prototype/index.html)
- [Requirements](docs/requirements.csv) and [test plan](docs/test-plan.csv)
- [Authentic YouTrack screenshots PDF](docs/YouTrack_Task_Screenshots.pdf)
- [Work breakdown](project-management/tasks.csv) and [YouTrack import preparation](project-management/youtrack-import.csv)

Repository: https://github.com/ayanvrsn/educator-digital-competencies (private).

Tracker: https://ayan-educator-diploma.youtrack.cloud/projects/EDU. Both were created on 22 October 2026. Recipient access is pending account details. The mapping from local W01-W40 planning references to actual YouTrack issues is in project-management/issue-map.csv.

Review package: [draft PR #1](https://github.com/ayanvrsn/educator-digital-competencies/pull/1). All report, diagram, prototype and tracker files are in `EDU-13/first-submission-preparation`; `main` currently contains the initial scaffold. Human review is pending.

## Open the prototype

Open `prototype/index.html` in a browser, or run from this directory:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765/prototype/`. State exists only in memory and is cleared on reload. Enter synthetic examples only. The administrator switch is a design demonstration, not authentication. Production setup/test commands will be added when the application is implemented; no non-existent npm commands are advertised.

## Review workflow

Use one permanent repository. Develop in task branches and use pull requests. Put the real tracker ID in the branch, commit and PR description; link the PR back to its task. Keep main as the reviewed baseline and request selected significant reviews from the supervisor at agreed checkpoints. Record work honestly from the actual start date. Do not backdate commits or fabricate review activity.

The live form requires `prob-period-1`; the DOCX says `pre-defense-1`. Create both immutable tags on the same exact submission commit only after the revision, access and required evidence are final. Use the `prob-period-1` URL in the form. The current review draft is not a tagged submission. See `project-management/submission-checklist.txt`.

## Privacy

Never commit secrets, signed personal eligibility documents, identifiable interviews or pupil records. Example configuration contains placeholders only. Store consent and participant contact keys separately from anonymised analysis.

The backlog now contains 40 actual issues: 30 tagged Diploma (research, design, application development, tests and evaluation) and 10 tagged Submission. The main board filters Diploma. The 19 later tasks have no due dates because the university has not yet announced the pre-defence/defence calendar. See project-management/backlog-guide.txt.
