# Futu OpenD Private Data Connector

Mira can read quote data from a local Futu OpenD session as a private,
authorized market-data source. The connector is quote-read-only: it does not
create a trading context and does not place, modify, or cancel orders.

## Privacy Boundary

Keep the following out of tracked files:

- account ids and trade permissions
- entitlement details
- raw vendor exports and retained quote datasets
- API logs that reveal private account or entitlement state

Use `private/mira-data.env` or environment variables for local settings. Use
`private/futu/` for emitted artifacts. The public repository may include
connector code, schemas, templates, and sanitized examples only.

## Local Configuration

Copy `templates/mira-data-config.example` to `private/mira-data.env` and set the
Futu fields:

```text
MIRA_FUTU_HOST=127.0.0.1
MIRA_FUTU_PORT=11111
MIRA_FUTU_DEFAULT_MARKET=US
MIRA_MARKET_DATA_DEFAULT_SOURCE=futu_opend
MIRA_LIVE_MARKET_DATA_SOURCE=futu_opend_local
MIRA_BROKER_DATA_PRIORITY=futu_opend_local,ibkr_gateway_local
```

Install the optional Python SDK in the runtime used for `mira_data`:

```sh
pip install futu-api
```

## Commands

Probe the local OpenD socket:

```sh
PYTHONPATH=tools python -m mira_data futu probe
```

Fetch a private market snapshot bundle:

```sh
PYTHONPATH=tools python -m mira_data fetch futu_market_price US.AAPL --out private/futu/US.AAPL
```

When `MIRA_MARKET_DATA_DEFAULT_SOURCE=futu_opend`, the generic market-price
family also routes to Futu OpenD:

```sh
PYTHONPATH=tools python -m mira_data fetch market_price AAPL --out private/futu/AAPL
```

Fetch historical bars:

```sh
PYTHONPATH=tools python -m mira_data fetch futu_historical_bars US.AAPL --out private/futu/US.AAPL-bars
```

Fetch a static option-chain contract list for an underlying:

```sh
PYTHONPATH=tools python -m mira_data fetch futu_option_chain US.AAPL --out private/futu/US.AAPL-options
```

Fetch futures contract metadata when you already know the concrete Futu futures
code:

```sh
PYTHONPATH=tools python -m mira_data fetch futu_future_info HK.<future-code> --out private/futu/futures
```

## Research Use

Futu OpenD data can support:

- live or delayed market-pricing context
- HK, US, A-share quote checks when the account has entitlements
- Singapore and Japan quote checks when the account has entitlements
- US/HK option-chain contract discovery, with dynamic option quotes fetched by
  passing returned option codes to `futu_market_price`
- futures contract metadata and snapshots when concrete futures codes are
  supplied and the account has matching entitlements
- private watchlist and technical context workflows

It should not be used as an autonomous execution path. Mira outputs remain
research support and must preserve the usual evidence, freshness, and
actionability boundaries.

## Local Entitlement Notes

Use `MIRA_FUTU_ENABLED_MARKETS` and `MIRA_FUTU_PERMISSION_NOTES` in
`private/mira-data.env` to record the local account's market-data permissions.
These notes are private machine state, not product state. Do not copy account
ids, quota counters, or raw vendor snapshots into tracked files.
