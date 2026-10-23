import type { ModuleId } from '../domain/assessment.ts';

// Original project questions carried over from the reviewed design prototype.
// This answer key belongs on the server; expose only getQuestionnaire() to clients.
export const ASSESSMENT_VERSION = 'diagnostic-2026-10-v1';

type Question = {
  id: string; moduleId: ModuleId; prompt: string;
  options: readonly string[]; correctOption: number;
};

export const QUESTIONS: readonly Question[] = [
  {
    "id": "M1-Q1",
    "moduleId": "M1",
    "prompt": "Which resource is the best starting point for a lesson?",
    "options": [
      "The most visually impressive one",
      "One that fits the learning objective and learners",
      "The first result in a search"
    ],
    "correctOption": 1
  },
  {
    "id": "M1-Q2",
    "moduleId": "M1",
    "prompt": "A diagram contains information that is essential to the task. What helps make it accessible?",
    "options": [
      "Add a meaningful text description",
      "Use colour alone to identify categories",
      "Replace the caption with a file name"
    ],
    "correctOption": 0
  },
  {
    "id": "M1-Q3",
    "moduleId": "M1",
    "prompt": "Before adapting a resource found online, what should you check?",
    "options": [
      "Only its download size",
      "Whether it is popular",
      "Its licence, source and suitability for the lesson"
    ],
    "correctOption": 2
  },
  {
    "id": "M2-Q1",
    "moduleId": "M2",
    "prompt": "What makes a quiz formative?",
    "options": [
      "It gives evidence that informs the next teaching step",
      "It contains at least twenty questions",
      "It has a strict timer"
    ],
    "correctOption": 0
  },
  {
    "id": "M2-Q2",
    "moduleId": "M2",
    "prompt": "Most learners choose the same incorrect option. What is the useful next action?",
    "options": [
      "Delete their answers",
      "Identify the misconception and plan a response",
      "Only display the class average"
    ],
    "correctOption": 1
  },
  {
    "id": "M2-Q3",
    "moduleId": "M2",
    "prompt": "Which feedback is most useful after an incorrect answer?",
    "options": [
      "Wrong",
      "Try harder",
      "An explanation of the mistake and a relevant next step"
    ],
    "correctOption": 2
  },
  {
    "id": "M3-Q1",
    "moduleId": "M3",
    "prompt": "A colleague only needs to read your resource. Which sharing setting fits?",
    "options": [
      "Public editing",
      "View access for the intended recipient",
      "Sharing your password"
    ],
    "correctOption": 1
  },
  {
    "id": "M3-Q2",
    "moduleId": "M3",
    "prompt": "Which example is appropriate for this training application?",
    "options": [
      "A fictitious class with no identifiable pupil details",
      "A screenshot of the real class register",
      "A list of pupils and their contact details"
    ],
    "correctOption": 0
  },
  {
    "id": "M3-Q3",
    "moduleId": "M3",
    "prompt": "How should an openly licensed image be reused?",
    "options": [
      "Assume all online images are unrestricted",
      "Remove the creator’s name",
      "Check the licence and provide the required attribution"
    ],
    "correctOption": 2
  }
];
