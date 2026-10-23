# Application implementation

The assessment domain logic is implemented in TypeScript under `domain/assessment.ts` (EDU-23). It validates nine scenario answers and three separate confidence responses, computes scores from the versioned answer key and returns field-level errors. The public questionnaire excludes correct answers.

This is the first part of EDU-23. Authentication, API handlers, database transactions, idempotent storage and attempt history are still required. Keep the assessment module and `content/assessment.server.ts` on the server when integrating them into Next.js. There is no production application yet.

Run `npm ci` and `npm run check` using the Node version in `.nvmrc`. The interactive design remains in `../prototype`; it is not yet connected to these functions.

`domain/recommendations.ts` implements the selection rule for EDU-29 / FR04. It selects the lowest-scoring incomplete module, breaks ties in M1/M2/M3 order and returns a reason with the topic and score. No assessment leads to the catalogue; completed modules lead to review. Confidence is excluded and the teacher can choose another topic. API and UI integration remain outstanding.
