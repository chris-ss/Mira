# Repro Impact Root-Cause Repair

- last_updated: 2026-07-03
- status: trial
- credibility_score: medium
- based_on_cases: GitHub issues #92, #94, #95, #96, #97 in `byteseek/Mira`

## Purpose

Use this method when handling repo-quality feedback, protocol complaints,
installer failures, schema drift, routing complexity, or agent-behavior
regressions.

The goal is not to defend the current design or accept every criticism. The
goal is to find the smallest correct repair that changes the failing path in
practice.

## Operating Rule

1. Reproduce the failure or state why it is not reproducible.
2. Separate fact, inference, and judgment in the complaint.
3. Identify real user impact: broken install, wrong answer, wasted context,
   degraded reasoning, maintenance burden, or only aesthetic preference.
4. Fix root cause, not symptoms.
5. Add a regression guard when the failure can recur: validator, example,
   compact entrypoint, template boundary, or explicit refresh trigger.
6. Avoid adding process unless it changes correctness, source quality,
   falsifiability, readiness, or next-route selection.

## Use / Do Not Use

Use for:

- GitHub issues and PR review feedback.
- Agent installer or runtime failures.
- Protocol bloat that wastes context or causes task drift.
- Schema or validator design that harms real workflow quality.

Do not use for:

- Market thesis judgment without source evidence.
- User preference memory unless the user explicitly asks.
- Broad refactors without a reproduced failure path.

## Failure Modes

- Treating a rude or emotional report as invalid without checking facts.
- Treating a correct bug report as a mandate for unrelated redesign.
- Fixing documentation while the executable validator still allows regression.
- Preserving every old field for compatibility and calling it a root-cause fix.
- Removing guardrails that prevent real research mistakes.

## Promotion Bar

Upgrade to `adopted` only after at least two completed repair cycles show:

- reproduced failures were correctly classified,
- fixes reduced recurrence or context cost,
- no material correctness guardrail was removed,
- follow-through confirms the new behavior in real use.
