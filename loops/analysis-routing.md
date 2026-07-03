# Mira Analysis Routing

This is the compact routing entrypoint for formal Mira work.

Use this file to decide the route without loading the full routing reference.
Load [analysis-routing-reference.md](analysis-routing-reference.md) only when a
selected route needs boundary detail that is not available in the route's own
loop or skill.

## Operating Standard

Every routing decision starts with the project repair standard:

1. Reproduce the user-visible problem or state why it is not reproducible.
2. Check real impact in practice, not only theoretical elegance.
3. Apply the smallest root-cause fix that changes the failing path.
4. Preserve correctness: facts, inferences and judgments stay separate.
5. Add a validator, example, or refresh trigger when the failure can recur.

Do not add routing fields, lenses, logs, or artifacts unless they change source
quality, falsifiability, readiness, or the next workflow.

## Route Selection

Read [../data/routing-index.csv](../data/routing-index.csv) first. It maps
`task_mode` to exactly one `primary_loop_or_skill` and a one-line trigger.
After the route hits, load only that loop or skill body.

Minimum routing fields:

- `primary_intent`
- `task_mode`
- `research_object`
- `market_scope`
- `time_boundary`
- `depth_mode`: `quick_map`, `standard`, or `deep_dive`
- `primary_loop_or_skill`
- `source_boundary`
- `private_state_action`

Add specialized fields only when the route needs them:

- live market data: `quote_time` / `publish_time`,
  `live_freshness_status`, `cross_check_status`
- calculation-heavy work: `quant_dependency`, `calculation_gate`
- actionability / position / portfolio work: `decision_pressure`,
  `framing_risk`, `disconfirmation_required`
- supplied files or vendor/API pulls: `ingestion_route`,
  `ingestion_artifacts`

## Question Lenses

Question lenses are optional helpers, not an upstream rewrite engine.

Default to `primary_question_lens=none`. Use a lens only when it improves this
route's evidence path, falsification path, quant gate, or progressive follow-up.
Never use a lens to change a clear deterministic task such as extracting facts,
checking a filing item, recalculating a metric, or summarizing a provided
document.

When useful, load [../data/question-expansion-lenses.md](../data/question-expansion-lenses.md)
and choose at most one primary lens. A second lens is allowed only when it
changes readiness or the next route. If the lens would broaden scope, surface it
as a follow-up or upgrade path instead of silently expanding the task.

## Evidence Surface

Depth controls artifact burden:

- `quick_map`: source notes are enough unless the user asks for a durable
  package.
- `standard`: use the selected package template and evidence artifacts.
- `deep_dive`: add calculation ledgers, source registries, route cards, and
  thesis artifacts only when they change the conclusion or auditability.

Use full `evidence-log.csv` only for durable research packages or retained
case artifacts. For quick triage, cite source notes plus `stale_after` /
`must_refresh_if`.

## Stop Rules

Return a downgrade instead of forcing a stronger answer when:

- source freshness cannot support the requested market judgment
- source quality is weak, conflicted, stale, or not independently checked
- a derived number lacks data, formula, or upstream source support
- an actionability answer lacks position, mandate, risk budget, or disconfirmation
- the dominant variable is not knowable with available evidence

Valid downgrade labels include `source_gap`, `calculation_gap`, `needs_refresh`,
`watch_only`, `not_actionable`, and `irreducible_uncertainty`.

## Reference

The old long-form routing document is preserved as
[analysis-routing-reference.md](analysis-routing-reference.md). Treat it as a
reference library, not the default prompt surface.
