import test from 'node:test';
import assert from 'node:assert/strict';
import { recommendModule } from '../src/domain/recommendations.ts';
import type { ModuleId, TopicScores } from '../src/domain/assessment.ts';

test('recommends the lowest-scoring incomplete module with its score and explanation', () => {
  const result = recommendModule({ M1: 3, M2: 1, M3: 2 });
  assert.equal(result.kind, 'recommendation');
  assert.equal(result.moduleId, 'M2');
  assert.match(result.reason, /Design online assessment.*1\/3/);
  assert.equal(result.mayChooseAnotherModule, true);
});

test('a completed module is excluded even when it has the lowest score', () => {
  assert.equal(recommendModule({ M1: 0, M2: 2, M3: 1 }, ['M1']).moduleId, 'M3');
});

test('equal scores follow M1, M2, M3 order among incomplete modules', () => {
  const scores = { M1: 1, M2: 1, M3: 1 };
  assert.equal(recommendModule(scores).moduleId, 'M1');
  assert.equal(recommendModule(scores, ['M1']).moduleId, 'M2');
  assert.match(recommendModule(scores).reason, /Equal scores/);
});

test('no assessment gives a catalogue without a personalised claim', () => {
  const result = recommendModule(null);
  assert.equal(result.kind, 'catalogue');
  assert.equal(result.moduleId, null);
  assert.doesNotMatch(result.reason, /lowest score/);
});

test('all completed modules give review instead of a new learning need', () => {
  for (const scores of [null, { M1: 0, M2: 1, M3: 2 }]) {
    const result = recommendModule(scores, ['M1', 'M2', 'M3']);
    assert.equal(result.kind, 'review');
    assert.equal(result.moduleId, null);
  }
});

test('duplicate completed IDs cannot hide a remaining module', () => {
  assert.equal(recommendModule({ M1: 0, M2: 1, M3: 2 }, ['M1', 'M1', 'M1']).moduleId, 'M2');
});

test('confidence has no influence on module selection', () => {
  const lowConfidence = { M1: 3, M2: 2, M3: 1, confidence: { M1: 1, M2: 1, M3: 1 } };
  const highConfidence = { ...lowConfidence, confidence: { M1: 3, M2: 3, M3: 3 } };
  assert.deepEqual(recommendModule(lowConfidence), recommendModule(highConfidence));
});

test('rejects missing, out-of-range, fractional and nonnumeric scores', () => {
  for (const scores of [{ M1: 0, M2: 1 }, { M1: -1, M2: 1, M3: 2 }, { M1: 4, M2: 1, M3: 2 },
    { M1: 1.5, M2: 1, M3: 2 }, { M1: NaN, M2: 1, M3: 2 }, { M1: '0', M2: 1, M3: 2 }]) {
    assert.throws(() => recommendModule(scores as TopicScores), RangeError);
  }
  assert.throws(() => recommendModule({ M1: 1, M2: 1, M3: 1 }, ['M4' as ModuleId]), RangeError);
});

test('every valid score combination and completion subset respects the selection rule', () => {
  const ids: ModuleId[] = ['M1', 'M2', 'M3'];
  for (let m1 = 0; m1 <= 3; m1++) for (let m2 = 0; m2 <= 3; m2++) for (let m3 = 0; m3 <= 3; m3++) {
    const scores = { M1: m1, M2: m2, M3: m3 };
    for (let mask = 0; mask < 8; mask++) {
      const completed = ids.filter((_, i) => mask & (1 << i));
      const result = recommendModule(scores, completed);
      if (result.kind !== 'recommendation') { assert.equal(mask, 7); continue; }
      assert.ok(!completed.includes(result.moduleId));
      for (const id of ids.filter(id => !completed.includes(id))) {
        assert.ok(result.score <= scores[id]);
        if (result.score === scores[id]) assert.ok(ids.indexOf(result.moduleId) <= ids.indexOf(id));
      }
    }
  }
});
