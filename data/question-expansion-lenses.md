# Mira Question Expansion Lenses

This file defines a light question-expansion helper for Mira routing and
progressive follow-up. It helps the agent ask a better research question only
when that improves the current route's evidence path.

This is not a second research framework. Use it only to sharpen the current
route. Default to `none` when a lens does not materially improve evidence
quality, falsifiability or next-route selection.

## Operating Rule

Lenses are optional. Default to `primary_question_lens=none`.

After `depth_mode` and `task_mode` are selected, choose a lens only when it
changes evidence quality, falsifiability, quant requirements, readiness, or the
next follow-up. Deterministic tasks should not receive a lens:

- extract a fact from a filing, table, transcript, or user-provided document
- recalculate a metric with a known formula
- summarize a provided source without thesis interpretation
- check whether a file, schema, route, or validation rule exists

When a lens is useful, choose at most one primary lens. A second lens is allowed
only when it changes readiness or the next route:

- `primary_question_lens`: the highest-value lens, or `none`.
- `selected_question_lenses`: complete ordered list of active question lenses,
  including `primary_question_lens`; omit or leave empty when the primary lens
  is `none`.
- `lens_selection_basis`: why the lens improves this specific question.
- `lens_data_required`: what evidence, baseline or calculation the lens needs.
- `lens_failure_mode`: how the lens can mislead if its requirements are absent.

If the lens requirements are unavailable, keep the answer at `working_view`,
`source_gap`, `calculation_gap`, `needs_refresh` or equivalent downgrade status.

`question_lens` sharpens the question before evidence work. It must not rewrite
the user's clear intent or broaden the object silently.
`selected_lenses` in single-equity routing selects analysis frameworks such as
variant perception. They do not replace each other.

Question expansion is scoped to the current route and depth. If a lens shows
that a broader scope or deeper package is needed, surface that as an explicit
upgrade path or progressive follow-up rather than silently expanding the task.
When the user asks for production-style work, complete the requested base task
first and put optional exploratory lenses after the answer.

## Lenses

### `comparison_association`

Use when the question is too absolute and needs a relative frame:

- peer comparison, customer / supplier read-through, index or factor context
- co-movement with macro, commodity, rate, FX, liquidity or industry variables
- relative valuation, relative growth, margin quality or revision path

Minimum discipline:

- name the comparator set or associated variable
- separate correlation, mechanism and causality
- require same-period and same-definition data before ranking

Failure mode:

- spurious association, cherry-picked peer set or treating co-movement as cause.

### `scale_shift`

Use when the question is framed at the wrong size:

- move up from event detail to thesis impact
- move down from broad theme to measurable variable
- connect company-level facts to segment, customer, unit economics or valuation
- connect single-name views to portfolio, industry or macro exposure only when
  the route permits it

Minimum discipline:

- state the original scale and target scale
- name what evidence survives the scale change
- avoid portfolio or sizing conclusions without holdings, mandate and risk data

Failure mode:

- overgeneralizing a narrow fact, or hiding an untested broad thesis inside a
  narrow event answer.

### `trend_dynamics`

Use when level alone is less informative than direction or rate of change:

- revenue, orders, backlog, margin, cash flow, revisions, valuation multiple
- macro, commodity, inventory, rates, employment or inflation time series
- price / volume reaction only as market context, not as thesis proof

Minimum discipline:

- identify level, first derivative and second derivative when relevant
- define window, frequency and baseline
- route to quant gate when the trend drives a durable conclusion

Failure mode:

- extrapolating a short series, ignoring base effects, or calling noise a trend.

### `anomaly_detection`

Use when the question depends on whether something is unusual:

- financial statement outliers, working capital, cash conversion, margin bridge
- valuation dislocation, estimate revision shock, price / volume gap
- peer divergence, customer concentration, inventory or order cancellation risk

Minimum discipline:

- define the baseline and materiality threshold
- separate data error, one-time item, cyclicality and structural change
- require a source or calculation note before upgrading the anomaly into thesis
  impact

Failure mode:

- treating every outlier as signal, or missing a real structural break by
  averaging it away.

## Follow-Up Use

Progressive follow-up may use a selected lens to generate a sharper next
question:

- comparison lens: "relative to which peer / variable?"
- scale lens: "should this be tested at event, segment, company, thesis or
  portfolio scale?"
- trend lens: "is the decisive variable level, direction, acceleration or
  persistence?"
- anomaly lens: "what baseline makes this abnormal, and what would prove it is
  structural?"

Do not expose these tokens by default in `quick_map`. Render them as natural
language unless the user asks for routing details or the output is a durable
artifact.
