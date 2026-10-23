# Verification

Run `npm ci` followed by `npm run check` with Node.js 24.19.0. The check includes TypeScript validation and the built-in Node test runner. All data in the tests is synthetic.

`assessment.test.ts` contains 19 tests for EDU-23 / FR02-FR03: nine mandatory answers, question identity, duplicate responses, invalid options, stale content versions, independent confidence values, server-computed scores and a public questionnaire without the answer key.

`recommendations.test.ts` contains nine tests for EDU-29 / FR04: the lowest incomplete topic, deterministic tie breaking, no assessment, all modules complete, unchanged selection across confidence values, invalid scores and duplicate completion IDs. One test checks the rule across all 64 score combinations and eight completion subsets (512 cases).

These are domain-function tests. They do not verify authenticated endpoints, database transactions, attempt history, real browser integration or learning outcomes. The wider application test plan is in `../docs/test-plan.csv` and report section 9. Browser checks of the separate local UX prototype are recorded in `../prototype/verification.txt`.
