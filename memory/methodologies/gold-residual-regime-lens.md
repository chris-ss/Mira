# Methodology Card: Gold Residual Regime Lens

- status: trial
- role: precious-metals macro-residual and risk-regime lens
- last_updated: 2026-07-03
- source_bucket: institutional; reverse_engineered; market_data; derived_internal
- source_quality: medium
- credibility_score: medium-low
- credibility_basis: The lens is reverse-engineered from one sell-side thematic report and is economically coherent, but the residual signal has not been independently rebuilt, backtested, or followed forward inside Mira.
- search_coverage: single-report reverse engineering plus existing Mira commodity, macro and top/bottom methods
- search_gaps: Needs independent data reconstruction, contrary literature, post-2024 follow-through, and failure cases where residual signals produced false regime calls.
- comparison_baseline: `commodity-cycle-analysis` plus `macro-regime-analysis` plus `top-bottom-risk-overlay` without a gold-specific residual check
- empirical_validation_mode: case backtest plus forward watch
- follow_through_plan: Rebuild the factor data and test the lens on 1973-1975, 1979-1982, 2006-2015, 2019-2024, and one live follow-forward window.

## Core Idea

Gold is a financialized commodity. Its price can be driven by physical supply and investment demand, but durable moves often pass through macro variables: dollar strength, real purchasing power, inflation expectations, crisis optionality and broad commodity purchasing power.

This lens asks whether gold is trading inside a macro-factor regime that can explain the price, or whether the residual between price and explainable macro factors has widened enough to indicate a fragile upside, bubble-like repricing, or possible new price plateau.

It is not a standalone valuation model, not a trading signal, and not a replacement for commodity balance work or gold-miner company research.

## Reverse-Engineered From

- Guolian Securities report dated 2024-05-21, `前瞻研究：黄金，遥遥领先的预言`, supplied by the user.
- Existing Mira `commodity-cycle-analysis` trial method.
- Existing Mira `macro-regime-analysis` trial method.
- Existing Mira `top-bottom-risk-overlay` trial method.

## Use When

- The object is gold, silver, a precious-metals ETF, a gold miner, or a precious-metals basket.
- The question depends on whether gold's move is explained by real rates, dollar, inflation, risk-off demand, central-bank or investment demand, or a residual/bubble-like repricing.
- A gold or gold-miner thesis needs to distinguish commodity beta from company alpha.
- A gold move looks disconnected from the usual real-rate / dollar / VIX explanation and the user asks whether the regime changed.

## Avoid When

- The object is a non-precious commodity where physical balance, inventory, curve and cost curve dominate.
- The user needs a company-first miner memo and gold price is only background.
- Current market data cannot be refreshed but the user wants a live or actionability conclusion.
- The analysis would rely on one report's model coefficients without rebuilding data or marking `calculation_gap`.

## Applies To

- `commodity-cycle-analysis` as a precious-metals sub-lens.
- `macro-regime-analysis` for gold, real-rate and dollar-sensitive assets.
- `top-bottom-risk-overlay` when gold is extended, bubble-like, washed out or in a regime-shift debate.
- `equity-research-core` commodity overlay for gold miners.
- `research-report-interpretation` when a report contributes a reusable gold residual framework.

## Core Question

Is gold's current price mostly explained by observable macro and commodity factors, or is the residual itself the key signal that the market is pricing a new dollar / inflation / crisis-optionality regime?

## Required Inputs

- gold spot or benchmark price with `quote_time` or `as_of_date`
- dollar proxy such as broad trade-weighted dollar or DXY, with source and date
- real-rate or purchasing-power proxy, with source and date
- inflation or commodity-price proxy, preferably a non-gold broad commodity index
- risk-off proxy such as VIX, credit spreads, geopolitical event map or volatility signal
- central-bank / ETF / futures positioning or investment-flow proxy when available
- current market narrative and consensus proxy where available
- for miners: realized price, hedges, AISC/cost, reserve/production, capex and political risk

## Primary Signal

The primary signal is the consistency or divergence between:

- `factor_explained_price`: what the macro / commodity factor stack can plausibly explain
- `actual_gold_price`: current gold price and trend
- `residual_direction`: whether gold is above or below factor-implied direction
- `residual_persistence`: whether the gap is brief noise or multi-window persistence
- `market_pricing`: whether investors already understand and price the same regime shift

If the factor model is not rebuilt, report this as qualitative residual mapping and mark `calculation_gap`.

## Minimal Factor Stack

Use this stack as a starting point, not as a fixed model:

- dollar external purchasing power: broad dollar index or DXY
- dollar domestic purchasing power / real-rate chain: real rates, purchasing-power proxy, CPI/PCE/PPI context
- crisis optionality: VIX, credit spreads, volatility or risk-off proxy
- commodity purchasing power: non-gold broad commodity index or CRB ex-gold proxy when available

Optional checks:

- central-bank reserve demand
- ETF holdings and futures positioning
- real yields by maturity
- gold/oil ratio as a rough cross-commodity signal

## Output Fields

For compact use, fill `templates/gold-residual-regime-check.csv`.

Minimum prose output:

- `gold_residual_lens`: `not_used`, `qualitative_only`, `recomputed`, or `calculation_gap`
- `factor_stack`
- `residual_state`: `explained`, `mild_divergence`, `large_divergence`, `mean_reverting`, `new_plateau_candidate`, or `source_gap`
- `dominant_macro_chain`
- `market_pricing`
- `risk_regime`
- `miner_transmission`, when mapping to equities
- `calculation_status`: `not_applicable`, `qualitative_proxy`, `recomputed`, or `calculation_gap`
- `confidence`
- `must_refresh_if`

## Integration Rules

- In `commodity-cycle-analysis`, use this only after the benchmark, physical balance and investment-demand context are mapped, unless gold is explicitly being treated as a macro asset.
- In `macro-regime-analysis`, use this to make the gold transmission chain specific; do not let it become a generic macro paragraph.
- In `top-bottom-risk-overlay`, treat residual widening as a risk-state input, not a timing signal.
- In gold-miner equity work, separate gold beta from company alpha before changing any thesis.
- In report interpretation, classify this as `method_delta` unless the factor data is independently rebuilt.

## Why It Works

The lens can add value because gold's macro factor sensitivity is time-varying. A persistent gap between gold and the usual dollar / real-rate / inflation / volatility explanation may indicate that the market is repricing a new macro regime, not merely reacting to one data print.

## Failure Mode

- The residual is fitted after the fact and mistaken for foresight.
- The model omits central-bank demand, ETF flows, positioning or sanctions/geopolitics, then overstates the residual.
- More factors reduce error mechanically but weaken economic meaning.
- A gold price call is transferred to miners without checking costs, hedges, reserve quality, jurisdiction risk and valuation.
- A bubble / new plateau label is used without an explicit `must_refresh_if`.
- The method becomes narrative because the factor stack was not rebuilt.

## Evidence Cost

Medium for qualitative use; high for recomputed use. Recomputed use needs a calculation ledger with data sources, transformations, model window, residual definition and sensitivity to factor choice.

## Speed Vs Depth

- `quick_map`: qualitative residual map, source gaps, and refresh triggers.
- `standard`: factor data pull, model or proxy residual, top/bottom risk state, and gold-miner transmission if needed.
- `deep_dive`: historical backtest, alternative factor stacks, residual sensitivity, miner scenario table and follow-through log.

## Comparison To Existing Methods

Compared with `commodity-cycle-analysis`, this lens is narrower and more financial: it is for precious metals where real rates, dollar, crisis optionality and investment flows can dominate physical balance.

Compared with `macro-regime-analysis`, it prevents gold analysis from staying at broad labels like `risk-off` or `real rates`; it forces a concrete factor stack and residual state.

Compared with `top-bottom-risk-overlay`, it supplies one gold-specific input to expectation burden and fragile-upside risk, but does not replace reaction quality, positioning or catalyst checks.

## Trial Design

Use the lens in:

- one historical 1970s inflation / oil-shock gold case
- one 2006-2015 gold boom and drawdown case
- one 2019-2024 gold regime-shift case
- one gold-miner equity case that separates commodity beta from company alpha
- one live follow-forward update after a major real-rate, dollar, VIX or central-bank demand change

## Falsification Conditions

Do not upgrade to adopted if:

- the residual cannot be reproduced from accessible sources
- it does not improve refresh triggers versus existing macro and commodity methods
- it produces frequent false bubble / new plateau labels
- it cannot distinguish gold bullion from miner equity transmission
- it mostly restates the Guolian report without independent validation

## Adoption Decision

Keep in `trial`. It can be used as a labeled lens in formal outputs only with source boundaries and calculation status stated.
