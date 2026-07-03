# Methodology Queue: Trial

- last_updated: 2026-07-03

## Purpose

记录准备在真实案例里验证的方法。

## Entry Format

- `method_name`
- `target_case`
- `expected_increment`
- `falsification_condition`

## Current Items

- `repro-impact-root-cause-repair`
  target_case: `GitHub issue triage`, `Mira protocol regressions`, `schema/routing/skill installer failures`, and future repo-quality complaints
  expected_increment: 对每个问题先建立可复现路径，再判断真实用户影响和实践成本，最后只做能改变失败路径的根因修复；避免为情绪化反馈做表面改名，也避免为了架构洁癖引入新的流程负担。
  falsification_condition: 如果该方法导致明显变慢、只产出“已记录但未修复”的口头回复、或修复缺少 validator / example / refresh trigger 而再次回归，就不升级到 `adopted`。
  notes: 由 2026-07-03 GitHub issues #92/#94/#95/#96/#97 triage 形成。核心判据：可复现、真实影响、根因性、正确性。
