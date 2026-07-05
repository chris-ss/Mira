"""Futu OpenD quote adapter.

This adapter reads from a user-run local Futu OpenD session. It is private-first
and quote-only: it never creates a trade context and never places orders.
"""

from __future__ import annotations

import datetime as _dt
import math
from typing import Optional

from .. import config, net
from ..canonical import POSTURES, CanonicalRecord, FetchResult

OPEND_ENDPOINT = "futu-opend://{host}:{port}"


def fetch_market_price(
    symbol: str,
    *,
    as_of: Optional[str] = None,
    market_scope: str = "multi",
) -> FetchResult:
    """Fetch a point-in-time market snapshot for ``symbol`` from local OpenD."""
    as_of = as_of or _dt.date.today().isoformat()
    code = _normalize_code(symbol)
    quote_ctx, endpoint, ft = _quote_context()
    try:
        ret, data = quote_ctx.get_market_snapshot([code])
        if ret != ft.RET_OK:
            raise net.FetchError(f"futu_source_gap: get_market_snapshot failed for {code}: {data}")
        row = _first_row(data)
        if not row:
            raise net.FetchError(f"futu_source_gap: no snapshot row returned for {code}")

        quote_time = _date_part(_field(row, "update_time")) or as_of
        currency = config.get("MIRA_FUTU_CURRENCY") or _default_currency(code)
        records = []
        for metric, field, unit in (
            ("last_price", "last_price", currency),
            ("open_price", "open_price", currency),
            ("high_price", "high_price", currency),
            ("low_price", "low_price", currency),
            ("previous_close", "prev_close_price", currency),
            ("volume", "volume", "shares"),
            ("turnover", "turnover", currency),
            ("turnover_rate", "turnover_rate", "percent"),
        ):
            value = _num(_field(row, field))
            if value is None:
                continue
            records.append(
                CanonicalRecord(
                    family="market_price",
                    research_object=code,
                    market_scope=market_scope,
                    metric=metric,
                    value=value,
                    unit=unit,
                    currency=currency if unit == currency else None,
                    period=quote_time,
                    period_type="point_in_time",
                    as_of_date=as_of,
                    source_date=quote_time,
                    posture=POSTURES["futu_opend"],
                    url_or_path=endpoint,
                    confidence="medium",
                    freshness_status="current",
                    provenance={
                        "code": code,
                        "name": _field(row, "name"),
                        "update_time": _field(row, "update_time"),
                        "suspension": _field(row, "suspension"),
                    },
                )
            )
        if not records:
            raise net.FetchError(f"futu_source_gap: no usable market fields for {code}")
        return FetchResult(records)
    finally:
        quote_ctx.close()


def fetch_historical_bars(
    symbol: str,
    *,
    as_of: Optional[str] = None,
    market_scope: str = "multi",
    start: str | None = None,
    end: str | None = None,
    ktype: str | None = None,
    autype: str | None = None,
) -> FetchResult:
    """Fetch daily or intraday K-line bars from local OpenD."""
    as_of = as_of or _dt.date.today().isoformat()
    code = _normalize_code(symbol)
    end = end or as_of
    start = start or config.get("MIRA_FUTU_HIST_START")
    ktype = ktype or config.get("MIRA_FUTU_HIST_KTYPE", "K_DAY") or "K_DAY"
    autype = autype or config.get("MIRA_FUTU_HIST_AUTYPE", "QFQ") or "QFQ"

    quote_ctx, endpoint, ft = _quote_context()
    try:
        ret, data, _page_req_key = quote_ctx.request_history_kline(
            code,
            start=start,
            end=end,
            ktype=getattr(ft.KLType, ktype),
            autype=getattr(ft.AuType, autype),
        )
        if ret != ft.RET_OK:
            raise net.FetchError(f"futu_source_gap: request_history_kline failed for {code}: {data}")
        rows = [_bar_row(row) for row in _iter_rows(data)]
        rows = [row for row in rows if row["date"]]
        if not rows:
            raise net.FetchError(f"futu_source_gap: no historical bars for {code}")

        currency = config.get("MIRA_FUTU_CURRENCY") or _default_currency(code)
        last = rows[-1]
        records = [
            CanonicalRecord(
                family="market_price",
                research_object=code,
                market_scope=market_scope,
                metric="last_close",
                value=last["close"],
                unit=currency,
                currency=currency,
                period=last["date"],
                period_type="point_in_time",
                as_of_date=as_of,
                source_date=last["date"],
                posture=POSTURES["futu_opend"],
                url_or_path=endpoint,
                freshness_status="current",
                provenance={"code": code, "ktype": ktype, "autype": autype},
            ),
            CanonicalRecord(
                family="market_price",
                research_object=code,
                market_scope=market_scope,
                metric="last_volume",
                value=last["volume"],
                unit="shares",
                period=last["date"],
                period_type="point_in_time",
                as_of_date=as_of,
                source_date=last["date"],
                posture=POSTURES["futu_opend"],
                url_or_path=endpoint,
                freshness_status="current",
                provenance={"code": code, "ktype": ktype, "autype": autype},
            ),
        ]
        series = {
            "name": f"futu_historical_bars-{code.replace('.', '_')}",
            "columns": ["date", "open", "high", "low", "close", "volume", "turnover"],
            "rows": rows,
        }
        return FetchResult(records, series=series)
    finally:
        quote_ctx.close()


def fetch_option_chain(
    symbol: str,
    *,
    as_of: Optional[str] = None,
    market_scope: str = "multi",
    start: str | None = None,
    end: str | None = None,
) -> FetchResult:
    """Fetch static option-chain contracts for an underlying from local OpenD."""
    as_of = as_of or _dt.date.today().isoformat()
    code = _normalize_code(symbol)
    quote_ctx, endpoint, ft = _quote_context()
    try:
        ret, data = quote_ctx.get_option_chain(code, start=start, end=end)
        if ret != ft.RET_OK:
            raise net.FetchError(f"futu_source_gap: get_option_chain failed for {code}: {data}")
        rows = list(_iter_rows(data))
        if not rows:
            raise net.FetchError(f"futu_source_gap: no option-chain rows for {code}")

        columns = _columns(data, rows)
        expiries = sorted({_field(row, "strike_time") for row in rows if _field(row, "strike_time")})
        source_date = expiries[0] if expiries else as_of
        records = [
            CanonicalRecord(
                family="options_surface",
                research_object=code,
                market_scope=market_scope,
                metric="option_contract_count",
                value=len(rows),
                unit="contracts",
                period=as_of,
                period_type="point_in_time",
                as_of_date=as_of,
                source_date=source_date,
                posture=POSTURES["futu_opend"],
                url_or_path=endpoint,
                confidence="medium",
                freshness_status="current",
                provenance={
                    "underlying": code,
                    "first_expiry": expiries[0] if expiries else None,
                    "last_expiry": expiries[-1] if expiries else None,
                },
            )
        ]
        series = {
            "name": f"futu_option_chain-{code.replace('.', '_')}",
            "columns": columns,
            "rows": rows,
        }
        return FetchResult(records, series=series)
    finally:
        quote_ctx.close()


def fetch_future_info(
    symbol: str,
    *,
    as_of: Optional[str] = None,
    market_scope: str = "multi",
) -> FetchResult:
    """Fetch futures contract metadata for concrete Futu future code(s)."""
    as_of = as_of or _dt.date.today().isoformat()
    codes = [_normalize_code(code) for code in symbol.split(",") if code.strip()]
    if not codes:
        raise net.FetchError("futu_source_gap: no futures codes supplied")
    quote_ctx, endpoint, ft = _quote_context()
    try:
        ret, data = quote_ctx.get_future_info(codes)
        if ret != ft.RET_OK:
            raise net.FetchError(f"futu_source_gap: get_future_info failed for {codes}: {data}")
        rows = list(_iter_rows(data))
        if not rows:
            raise net.FetchError(f"futu_source_gap: no futures info rows for {codes}")

        records = []
        for row in rows:
            code = _field(row, "code") or codes[0]
            currency = _field(row, "price_currency") or _default_currency(code)
            records.append(
                CanonicalRecord(
                    family="market_price",
                    research_object=code,
                    market_scope=market_scope,
                    metric="future_contract_size",
                    value=_num(_field(row, "size")),
                    unit=_field(row, "size_unit") or "contracts",
                    currency=currency if currency != "not_applicable" else None,
                    period=as_of,
                    period_type="point_in_time",
                    as_of_date=as_of,
                    source_date=as_of,
                    posture=POSTURES["futu_opend"],
                    url_or_path=endpoint,
                    confidence="medium",
                    freshness_status="current",
                    provenance={k: _field(row, k) for k in (
                        "name", "owner", "exchange", "type", "price_currency",
                        "trade_time", "time_zone", "last_trade_time",
                    )},
                )
            )
        series = {
            "name": f"futu_future_info-{codes[0].replace('.', '_')}",
            "columns": _columns(data, rows),
            "rows": rows,
        }
        return FetchResult(records, series=series)
    finally:
        quote_ctx.close()


def probe() -> str:
    """Connect to OpenD and close immediately, returning the endpoint."""
    quote_ctx, endpoint, _ft = _quote_context()
    quote_ctx.close()
    return endpoint


def _quote_context():
    try:
        import futu as ft  # type: ignore
    except ImportError as exc:
        raise net.FetchError(
            "futu_dependency_gap: install optional dependency 'futu-api' to use Futu OpenD"
        ) from exc

    host = config.get("MIRA_FUTU_HOST", "127.0.0.1") or "127.0.0.1"
    port = _int_cfg("MIRA_FUTU_PORT", 11111)
    timeout = _float_cfg("MIRA_FUTU_TIMEOUT", 10.0)
    endpoint = OPEND_ENDPOINT.format(host=host, port=port)
    try:
        quote_ctx = ft.OpenQuoteContext(host=host, port=port)
        if hasattr(quote_ctx, "set_keep_alive"):
            quote_ctx.set_keep_alive(True)
        if hasattr(quote_ctx, "set_conn_timeout"):
            quote_ctx.set_conn_timeout(timeout)
        return quote_ctx, endpoint, ft
    except Exception as exc:
        raise net.FetchError(f"futu_connection_gap: could not connect to {endpoint}: {exc}") from exc


def _normalize_code(symbol: str) -> str:
    raw = symbol.strip()
    if "." in raw:
        market, code = raw.split(".", 1)
        return f"{market.upper()}.{code.upper()}"
    market = config.get("MIRA_FUTU_DEFAULT_MARKET", "US") or "US"
    return f"{market.upper()}.{raw.upper()}"


def _first_row(data) -> dict:
    rows = list(_iter_rows(data))
    return rows[0] if rows else {}


def _iter_rows(data):
    if hasattr(data, "to_dict"):
        yield from data.to_dict("records")
    elif isinstance(data, list):
        yield from data
    elif isinstance(data, dict):
        yield data


def _columns(data, rows: list[dict]) -> list[str]:
    if hasattr(data, "columns"):
        return [str(col) for col in data.columns]
    cols = []
    for row in rows:
        for key in row:
            if key not in cols:
                cols.append(key)
    return cols


def _bar_row(row) -> dict:
    return {
        "date": _date_part(_field(row, "time_key")) or _date_part(_field(row, "date")) or "",
        "open": _num(_field(row, "open")),
        "high": _num(_field(row, "high")),
        "low": _num(_field(row, "low")),
        "close": _num(_field(row, "close")),
        "volume": _nonnegative(_field(row, "volume")),
        "turnover": _nonnegative(_field(row, "turnover")),
    }


def _field(row, name: str):
    if isinstance(row, dict):
        return row.get(name)
    return getattr(row, name, None)


def _date_part(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text.split(" ", 1)[0]


def _default_currency(code: str) -> str:
    market = code.split(".", 1)[0]
    return {
        "US": "USD",
        "HK": "HKD",
        "SH": "CNY",
        "SZ": "CNY",
        "CN": "CNY",
        "SG": "SGD",
        "JP": "JPY",
    }.get(market, "not_applicable")


def _num(value):
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


def _nonnegative(value):
    f = _num(value)
    if f is None or f < 0:
        return None
    return f


def _int_cfg(key: str, default: int) -> int:
    try:
        return int(config.get(key, str(default)) or default)
    except ValueError:
        return default


def _float_cfg(key: str, default: float) -> float:
    try:
        return float(config.get(key, str(default)) or default)
    except ValueError:
        return default
