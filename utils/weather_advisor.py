"""Weather-based farming advice for Malawi tobacco farmers."""

from __future__ import annotations

import random
from datetime import date
from typing import Any

from utils.i18n import t

DEFAULT_WEATHER = {
    "location_en": "Central Region, Malawi",
    "location_ny": "Central Region, Malawi",
    "date": str(date.today()),
    "temp_c": 28,
    "humidity_pct": 65,
    "rain_mm": 3,
    "rain_forecast_mm": 12,
    "wind_kmh": 8,
}


def get_mock_weather(seed: int | None = None, lang: str = "en") -> dict[str, Any]:
    rng = random.Random(seed or date.today().toordinal())
    base = DEFAULT_WEATHER.copy()
    base["temp_c"] = rng.randint(22, 34)
    base["humidity_pct"] = rng.randint(45, 90)
    base["rain_mm"] = rng.randint(0, 8)
    base["rain_forecast_mm"] = rng.randint(0, 25)
    base["wind_kmh"] = rng.randint(5, 20)
    base["location"] = t("location", lang)
    return base


def analyze_weather(
    temp_c: float,
    humidity_pct: float,
    rain_mm: float,
    rain_forecast_mm: float,
    lang: str = "en",
) -> dict[str, Any]:
    alerts: list[dict[str, str]] = []
    advice: list[str] = []

    if rain_forecast_mm >= 15 or rain_mm >= 10:
        alerts.append({
            "type": "rain", "level": "red",
            "msg": "Mvula yambiri ikuyembekezeka — chiwopsezo cha kuwononga masamba" if lang == "ny"
            else "Heavy rain expected — risk of leaf damage",
        })
        advice.append("Musawopsye fodya lero." if lang == "ny" else "Do not dry tobacco today.")
        advice.append("Dikirani kupopera mpaka masamba atakhala owuma." if lang == "ny" else "Delay spraying until leaves are dry.")
    elif rain_forecast_mm >= 5:
        alerts.append({
            "type": "rain", "level": "yellow",
            "msg": "Mvula yochepa ingathe kubwera" if lang == "ny" else "Light rain possible",
        })
        advice.append("Tetezani zomera za nursery ngati mungathe." if lang == "ny" else "Cover nursery seedlings if possible.")
    else:
        alerts.append({
            "type": "rain", "level": "green",
            "msg": "Chiwopsezo cha mvula chochepa lero" if lang == "ny" else "Low rain risk today",
        })
        advice.append("Tsiku labwino logwira ntchito m'munda." if lang == "ny" else "Good day for field work.")

    if temp_c >= 35:
        alerts.append({
            "type": "heat", "level": "red",
            "msg": "Kutentha kwakukulu — chiwopsezo cha kuwononga masamba" if lang == "ny"
            else "Extreme heat — leaf scorch risk",
        })
        advice.append("Phirimitsani madzi mmamawa. Perekani mthunzi kwa nursery." if lang == "ny" else "Water early morning. Provide shade for nursery.")
    elif temp_c >= 32:
        alerts.append({
            "type": "heat", "level": "yellow",
            "msg": "Kutentha kwakukulu — yang'anani kufota" if lang == "ny"
            else "High temperature — watch for wilting",
        })
        advice.append("Phirimitsani madzi mmamawa kapena madzulo." if lang == "ny" else "Irrigate in early morning or late evening.")
    else:
        alerts.append({
            "type": "heat", "level": "green",
            "msg": "Kutentha kwavomerezeka pa ntchito ya m'munda" if lang == "ny"
            else "Temperature OK for field work",
        })

    if humidity_pct >= 85:
        alerts.append({
            "type": "disease", "level": "yellow",
            "msg": "Kunyowa kwakukulu — chiwopsezo cha matenda chikukula" if lang == "ny"
            else "High humidity — disease risk increases",
        })
        advice.append("Onani masamba kuti muone mould ndi malo after mvula." if lang == "ny" else "Check leaves for mold and spots after rain.")

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
