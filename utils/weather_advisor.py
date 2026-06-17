"""Weather-based farming advice for Malawi tobacco farmers."""

from __future__ import annotations

import random
from datetime import date
from typing import Any

# Realistic Lilongwe-area mock values (API-ready structure)
DEFAULT_WEATHER = {
    "location": "Central Region, Malawi",
    "date": str(date.today()),
    "temp_c": 28,
    "humidity_pct": 65,
    "rain_mm": 3,
    "rain_forecast_mm": 12,
    "wind_kmh": 8,
}


def get_mock_weather(seed: int | None = None) -> dict[str, Any]:
    """Return stable mock weather for offline use."""
    rng = random.Random(seed or date.today().toordinal())
    base = DEFAULT_WEATHER.copy()
    base["temp_c"] = rng.randint(22, 34)
    base["humidity_pct"] = rng.randint(45, 90)
    base["rain_mm"] = rng.randint(0, 8)
    base["rain_forecast_mm"] = rng.randint(0, 25)
    base["wind_kmh"] = rng.randint(5, 20)
    return base


def analyze_weather(
    temp_c: float,
    humidity_pct: float,
    rain_mm: float,
    rain_forecast_mm: float,
) -> dict[str, Any]:
    """Generate simple risk flags and farmer advice."""
    alerts: list[dict[str, str]] = []
    advice: list[str] = []

    if rain_forecast_mm >= 15 or rain_mm >= 10:
        alerts.append({"type": "rain", "level": "red", "msg": "Heavy rain expected — risk of leaf damage"})
        advice.append("Do not dry tobacco today.")
        advice.append("Delay spraying until leaves are dry.")
    elif rain_forecast_mm >= 5:
        alerts.append({"type": "rain", "level": "yellow", "msg": "Light rain possible"})
        advice.append("Cover nursery seedlings if possible.")
    else:
        alerts.append({"type": "rain", "level": "green", "msg": "Low rain risk today"})
        advice.append("Good day for field work.")

    if temp_c >= 35:
        alerts.append({"type": "heat", "level": "red", "msg": "Extreme heat — leaf scorch risk"})
        advice.append("Water early morning. Provide shade for nursery.")
    elif temp_c >= 32:
        alerts.append({"type": "heat", "level": "yellow", "msg": "High temperature — watch for wilting"})
        advice.append("Irrigate in early morning or late evening.")
    else:
        alerts.append({"type": "heat", "level": "green", "msg": "Temperature OK for field work"})

    if humidity_pct >= 85:
        alerts.append({"type": "disease", "level": "yellow", "msg": "High humidity — disease risk increases"})
        advice.append("Check leaves for mold and spots after rain.")

    # Overall risk for dashboard
    levels = [a["level"] for a in alerts]
    if "red" in levels:
        overall = "red"
    elif "yellow" in levels:
        overall = "yellow"
    else:
        overall = "green"

    return {
        "alerts": alerts,
        "advice": advice,
        "overall_risk": overall,
        "good_harvest_day": overall == "green" and temp_c < 32 and rain_forecast_mm < 5,
    }
