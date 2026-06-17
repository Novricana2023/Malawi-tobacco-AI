"""Market price data and selling advice for tobacco farmers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _mock_prices_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.date_range("2025-01-01", periods=12, freq="W"),
            "Price_MWK_per_kg": [850, 870, 890, 920, 910, 880, 860, 840, 830, 850, 900, 950],
            "Grade": ["Burley"] * 12,
        }
    )


def load_prices() -> pd.DataFrame:
    csv_path = DATA_DIR / "mock_prices.csv"
    try:
        if csv_path.exists():
            df = pd.read_csv(csv_path, parse_dates=["Date"])
            if "Price_MWK_per_kg" not in df.columns and "Price" in df.columns:
                df = df.rename(columns={"Price": "Price_MWK_per_kg"})
            if df.empty or "Price_MWK_per_kg" not in df.columns:
                return _mock_prices_df()
            return df.sort_values("Date")
    except Exception:
        pass
    return _mock_prices_df()


def get_market_advice(df: pd.DataFrame | None = None, lang: str = "en") -> dict[str, Any]:
    df = df if df is not None else load_prices()
    prices = df["Price_MWK_per_kg"].astype(float)
    current = float(prices.iloc[-1])
    avg_4 = float(prices.tail(4).mean())
    avg_all = float(prices.mean())
    trend = current - float(prices.iloc[-2]) if len(prices) > 1 else 0

    if current >= avg_all * 1.05 and trend > 0:
        action = "Mitengo ikwera — ganizirani kugulitsa" if lang == "ny" else "Prices are high this week → consider selling"
        signal = "green"
    elif current <= avg_all * 0.92:
        action = "Dikirani kukolola ngati mitengo ili pansi" if lang == "ny" else "Hold harvest if prices are low — wait for better week"
        signal = "red"
    else:
        action = "Mitengo ikukhala yofanana — gulitsani ngati fodya yakonzeka" if lang == "ny" else "Prices are stable — sell if crop is ready and properly cured"
        signal = "yellow"

    return {
        "current_price_mwk": round(current, 0),
        "avg_4_week_mwk": round(avg_4, 0),
        "avg_all_mwk": round(avg_all, 0),
        "weekly_change": round(trend, 0),
        "action": action,
        "signal": signal,
        "dataframe": df,
    }
