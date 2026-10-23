import { ASSESSMENT_VERSION, QUESTIONS } from '../content/assessment.server.ts';

export const MODULE_IDS = ['M1', 'M2', 'M3'] as const;
export type ModuleId = typeof MODULE_IDS[number];
export type TopicScores = Record<ModuleId, number>;
export type Confidence = Record<ModuleId, 1 | 2 | 3>;
export type Answer = { questionId: string; optionIndex: number };
export type FieldError = { field: string; message: string };

export class AssessmentValidationError extends Error {
  readonly errors: FieldError[];
  constructor(errors: FieldError[]) {
    super('Check the assessment responses.');
    this.name = 'AssessmentValidationError';
    this.errors = errors;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

// The public questionnaire never contains the scoring key. Call this on the server;
// do not import assessment.server.ts or this module into a browser bundle.
export function getQuestionnaire() {
  return {
    contentVersion: ASSESSMENT_VERSION,
    questions: QUESTIONS.map(({ correctOption: _key, ...question }) => ({
      ...question, options: [...question.options],
    })),
  };
}

export function scoreAssessment(input: unknown) {
  if (!isRecord(input)) {
    throw new AssessmentValidationError([{ field: 'body', message: 'Submit an assessment object.' }]);
  }
  const errors: FieldError[] = [];
  if (input.contentVersion !== ASSESSMENT_VERSION) {
    errors.push({ field: 'contentVersion', message: 'Reload the current questionnaire before submitting.' });
  }
  const answers = new Map<string, number>();
  if (!Array.isArray(input.answers) || input.answers.length !== QUESTIONS.length) {
    errors.push({ field: 'answers', message: 'Answer all nine questions exactly once.' });
  }
  if (Array.isArray(input.answers)) {
    input.answers.forEach((answer: unknown, index: number) => {
      const field = `answers.${index}`;
      if (!isRecord(answer) || typeof answer.questionId !== 'string') {
        errors.push({ field, message: 'Provide a question ID and selected option.' });
        return;
      }
      const question = QUESTIONS.find(q => q.id === answer.questionId);
      if (!question) {
        errors.push({ field: `${field}.questionId`, message: 'Unknown question.' });
        return;
      }
      if (answers.has(question.id)) {
        errors.push({ field: `${field}.questionId`, message: 'Answer each question only once.' });
        return;
      }
      if (typeof answer.optionIndex !== 'number' || !Number.isInteger(answer.optionIndex)
        || answer.optionIndex < 0 || answer.optionIndex >= question.options.length) {
        errors.push({ field: `${field}.optionIndex`, message: 'Choose one of the listed options.' });
        return;
      }
      answers.set(question.id, answer.optionIndex);
    });
  }
  for (const question of QUESTIONS) {
    if (!answers.has(question.id)) {
      errors.push({ field: `answers.${question.id}`, message: 'Choose an answer for this question.' });
    }
  }
  const confidence: Confidence = { M1: 1, M2: 1, M3: 1 };
  for (const id of MODULE_IDS) {
    const value = isRecord(input.confidence) && Object.hasOwn(input.confidence, id)
      ? input.confidence[id] : undefined;
    if (value !== 1 && value !== 2 && value !== 3) {
      errors.push({ field: `confidence.${id}`, message: 'Choose a confidence response from 1 to 3.' });
    } else {
      confidence[id] = value;
    }
  }
  if (errors.length) throw new AssessmentValidationError(errors);

  const scores: TopicScores = { M1: 0, M2: 0, M3: 0 };
  for (const question of QUESTIONS) {
    if (answers.get(question.id) === question.correctOption) scores[question.moduleId]++;
  }
  return {
    contentVersion: ASSESSMENT_VERSION,
    scoringVersion: 'scenario-count-v1',
    answers: QUESTIONS.map(q => ({ questionId: q.id, optionIndex: answers.get(q.id)! })),
    scores,
    confidence,
    maximumPerTopic: 3 as const,
  };
}
