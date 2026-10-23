import { MODULE_IDS } from './assessment.ts';
import type { ModuleId, TopicScores } from './assessment.ts';

export const RECOMMENDATION_VERSION = 'lowest-incomplete-v1';
const TITLES: Record<ModuleId, string> = {
  M1: 'Create digital resources',
  M2: 'Design online assessment',
  M3: 'Share resources responsibly',
};

export type Recommendation = {
  kind: 'recommendation'; moduleId: ModuleId; score: number;
  reason: string; ruleVersion: string; mayChooseAnotherModule: true;
} | {
  kind: 'catalogue' | 'review'; moduleId: null;
  reason: string; ruleVersion: string; mayChooseAnotherModule: true;
};

// Supply scores and completed module IDs from the learner's server-side records.
// Confidence is intentionally not an input to this selection rule.
export function recommendModule(scores: TopicScores | null, completed: readonly ModuleId[] = []): Recommendation {
  if (scores !== null && (typeof scores !== 'object' || Array.isArray(scores)
    || MODULE_IDS.some(id => !Object.hasOwn(scores, id) || !Number.isInteger(scores[id]) || scores[id] < 0 || scores[id] > 3))) {
    throw new RangeError('Each module must have an integer scenario score from 0 to 3.');
  }
  if (!Array.isArray(completed) || completed.some(id => !MODULE_IDS.includes(id))) {
    throw new RangeError('Completed modules must use the known module IDs.');
  }
  const remaining = MODULE_IDS.filter(id => !completed.includes(id));
  if (remaining.length === 0) {
    return { kind: 'review', moduleId: null, reason: 'All modules are complete. You can revisit any lesson.', ruleVersion: RECOMMENDATION_VERSION, mayChooseAnotherModule: true };
  }
  if (scores === null) {
    return { kind: 'catalogue', moduleId: null, reason: 'Choose a module or take the assessment for a suggested starting point.', ruleVersion: RECOMMENDATION_VERSION, mayChooseAnotherModule: true };
  }
  // Iteration order is the documented tie-break order: M1, M2, then M3.
  let selected = remaining[0]!;
  for (const id of remaining) if (scores[id] < scores[selected]) selected = id;
  const score = scores[selected];
  const tied = remaining.filter(id => scores[id] === score).length > 1;
  const reason = `${TITLES[selected]} is a suggested starting point: ${score}/3 scenario answers correct, the lowest score among your incomplete modules.${tied ? ' Equal scores use the order M1, M2, M3.' : ''} You can choose a different module.`;
  return { kind: 'recommendation', moduleId: selected, score, reason, ruleVersion: RECOMMENDATION_VERSION, mayChooseAnotherModule: true };
}
