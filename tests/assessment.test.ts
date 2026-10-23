import test from 'node:test';
import assert from 'node:assert/strict';
import { getQuestionnaire, scoreAssessment, AssessmentValidationError } from '../src/domain/assessment.ts';

function submission() {
  return {
    contentVersion: 'diagnostic-2026-10-v1',
    answers: [1, 0, 2, 0, 1, 2, 1, 0, 2].map((optionIndex, i) => ({
      questionId: `M${Math.floor(i / 3) + 1}-Q${i % 3 + 1}`, optionIndex,
    })),
    confidence: { M1: 1, M2: 2, M3: 3 },
  };
}

test('nine scenario answers give separate topic scores and preserve version metadata', () => {
  const input = submission();
  input.answers[0]!.optionIndex = 0;
  input.answers[3]!.optionIndex = 1;
  input.answers[4]!.optionIndex = 2;
  const result = scoreAssessment(input);
  assert.deepEqual(result.scores, { M1: 2, M2: 1, M3: 3 });
  assert.deepEqual(result.confidence, { M1: 1, M2: 2, M3: 3 });
  assert.equal(result.contentVersion, 'diagnostic-2026-10-v1');
  assert.equal(result.scoringVersion, 'scenario-count-v1');
});

test('client scores and confidence cannot change scenario correctness', () => {
  const input = submission();
  input.answers.forEach(answer => { answer.optionIndex = (answer.optionIndex + 1) % 3; });
  const result = scoreAssessment({ ...input, scores: { M1: 3, M2: 3, M3: 3 }, confidence: { M1: 3, M2: 3, M3: 3 } });
  assert.deepEqual(result.scores, { M1: 0, M2: 0, M3: 0 });
});

test('question order does not change the result or stored answer order', () => {
  const input = submission();
  assert.deepEqual(scoreAssessment({ ...input, answers: [...input.answers].reverse() }), scoreAssessment(input));
});

for (const input of [null, [], 'answers', 42]) {
  test(`rejects a non-object request: ${JSON.stringify(input)}`, () => {
    assert.throws(() => scoreAssessment(input), AssessmentValidationError);
  });
}

test('an omitted answer produces a field-level error', () => {
  const input = submission(); input.answers.pop();
  assert.throws(() => scoreAssessment(input), (error: unknown) =>
    error instanceof AssessmentValidationError && error.errors.some(e => e.field === 'answers.M3-Q3'));
});

test('duplicate and unknown questions are rejected', () => {
  const input = submission(); input.answers[8] = { ...input.answers[0]! };
  assert.throws(() => scoreAssessment(input), AssessmentValidationError);
  input.answers[8] = { questionId: 'M4-Q1', optionIndex: 0 };
  assert.throws(() => scoreAssessment(input), AssessmentValidationError);
});

for (const optionIndex of [-1, 3, 0.5, '1', null, NaN, Infinity]) {
  test(`rejects an invalid option: ${String(optionIndex)}`, () => {
    const input = submission();
    assert.throws(() => scoreAssessment({ ...input, answers: [{ ...input.answers[0], optionIndex }, ...input.answers.slice(1)] }), AssessmentValidationError);
  });
}

test('all three confidence responses must be valid and present', () => {
  for (const confidence of [null, {}, { M1: 1, M2: 2 }, { M1: '1', M2: 2, M3: 3 }, { M1: 4, M2: 2, M3: 3 }]) {
    assert.throws(() => scoreAssessment({ ...submission(), confidence }), AssessmentValidationError);
  }
});

test('outdated content cannot silently be rescored with the current answer key', () => {
  assert.throws(() => scoreAssessment({ ...submission(), contentVersion: 'old' }), AssessmentValidationError);
});

test('public questions omit the key and cannot mutate the scoring content', () => {
  const publicData = getQuestionnaire();
  assert.equal(publicData.questions.length, 9);
  assert.ok(publicData.questions.every(q => !('correctOption' in q)));
  publicData.questions[0]!.options[0] = 'Changed in browser';
  assert.notEqual(getQuestionnaire().questions[0]!.options[0], 'Changed in browser');
});
