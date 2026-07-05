#!/usr/bin/env python3
"""Regression tests for the optional Futu OpenD adapter.

The tests use a fake ``futu`` module, so they do not require OpenD, credentials,
market-data entitlements, or the optional ``futu-api`` package.
"""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.mira_data import __main__ as cli
from tools.mira_data import config, net
from tools.mira_data.adapters import futu_opend


class FakeQuoteContext:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.closed = False

    def set_keep_alive(self, _enabled: bool) -> None:
        pass

    def set_conn_timeout(self, _timeout: float) -> None:
        pass

    def close(self) -> None:
        self.closed = True

    def get_market_snapshot(self, codes: list[str]):
        return 0, [
            {
                "code": codes[0],
                "name": "Apple",
                "update_time": "2026-07-02 15:59:00",
                "last_price": "200.5",
                "open_price": "198.0",
                "high_price": "201.0",
                "low_price": "197.5",
                "prev_close_price": "199.0",
                "volume": "123456",
                "turnover": "24691200",
                "turnover_rate": "0.5",
                "suspension": False,
            }
        ]


def _fake_futu_module() -> types.SimpleNamespace:
    return types.SimpleNamespace(RET_OK=0, OpenQuoteContext=FakeQuoteContext)


def test_missing_optional_dependency_is_source_gap() -> None:
    with mock.patch.dict(sys.modules, {"futu": None}):
        try:
            futu_opend.probe()
        except net.FetchError as exc:
            assert "futu_dependency_gap" in str(exc)
        else:
            raise AssertionError("expected FetchError when futu-api is missing")

    print("ok missing futu-api reports a source gap")


def test_normalize_code_uses_default_market() -> None:
    with mock.patch.dict(os.environ, {"MIRA_FUTU_DEFAULT_MARKET": "HK"}, clear=False):
        config.reset_cache()
        assert futu_opend._normalize_code("00700") == "HK.00700"
        assert futu_opend._normalize_code("us.aapl") == "US.AAPL"

    print("ok Futu symbols use default market only when unprefixed")


def test_market_snapshot_maps_canonical_records() -> None:
    env = {
        "MIRA_FUTU_HOST": "127.0.0.1",
        "MIRA_FUTU_PORT": "11111",
        "MIRA_FUTU_DEFAULT_MARKET": "US",
    }
    with (
        mock.patch.dict(os.environ, env, clear=False),
        mock.patch.dict(sys.modules, {"futu": _fake_futu_module()}),
    ):
        config.reset_cache()
        result = futu_opend.fetch_market_price("AAPL", as_of="2026-07-02")

    metrics = {record.metric: record for record in result.records}
    assert metrics["last_price"].value == 200.5
    assert metrics["last_price"].research_object == "US.AAPL"
    assert metrics["last_price"].posture.source_id == "futu_opend_local"
    assert metrics["volume"].unit == "shares"
    print("ok Futu market snapshot maps to canonical records")


def test_default_market_provider_routes_generic_market_price() -> None:
    with mock.patch.dict(os.environ, {"MIRA_MARKET_DATA_DEFAULT_SOURCE": "futu_opend"}, clear=False):
        config.reset_cache()
        assert cli._effective_fetch_family("market_price") == "futu_market_price"
        assert cli._effective_fetch_family("company_financials") == "company_financials"

    print("ok configured default provider routes generic market_price")


def main() -> int:
    test_missing_optional_dependency_is_source_gap()
    test_normalize_code_uses_default_market()
    test_market_snapshot_maps_canonical_records()
    test_default_market_provider_routes_generic_market_price()
    print("mira_data_futu_tests: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
