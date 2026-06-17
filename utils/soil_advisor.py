"""Soil suitability evaluation for tobacco in Malawi."""

from __future__ import annotations

from typing import Any

SOIL_TYPES = ["Loamy", "Sandy", "Clay"]
MOISTURE_LEVELS = ["Dry", "Medium", "Wet"]


def evaluate_soil(
    soil_type: str,
    ph: float | None,
    moisture: str,
) -> dict[str, Any]:
    """
    Rule-based soil assessment for smallholder tobacco.
    pH can be None if farmer does not know.
    """
    score = 50
    tips: list[str] = []
    fertilizer: str

    soil_scores = {"Loamy": 25, "Sandy": 10, "Clay": -5}
    score += soil_scores.get(soil_type, 0)

    if ph is not None:
        if 5.5 <= ph <= 6.5:
            score += 20
            tips.append("pH is in the ideal range for tobacco (5.5–6.5).")
        elif 5.0 <= ph < 5.5 or 6.5 < ph <= 7.0:
            score += 5
            tips.append("pH is acceptable but not ideal. Consider soil testing at extension office.")
        else:
            score -= 15
            tips.append("pH is outside ideal range. Lime or sulfur may be needed — ask extension worker.")
    else:
        tips.append("pH unknown — visit your agriculture extension office for free soil testing.")

    moisture_scores = {"Dry": -10, "Medium": 15, "Wet": -20}
    score += moisture_scores.get(moisture, 0)

    if moisture == "Dry":
        tips.append("Irrigate lightly in early morning. Mulch around plants to keep moisture.")
    elif moisture == "Wet":
        tips.append("Improve drainage with ridges. Avoid working field when waterlogged.")
    else:
        tips.append("Moisture level is good. Maintain with regular morning checks.")

    if soil_type == "Sandy":
        fertilizer = "Apply compost or well-rotted manure before transplanting. Split NPK fertilizer in 2 doses."
        tips.append("Sandy soil loses nutrients fast — add organic matter every season.")
    elif soil_type == "Clay":
        fertilizer = "Use lighter NPK dose. Add sand and compost to improve structure."
        tips.append("Clay holds water — plant on ridges to prevent root rot.")
    else:
        fertilizer = "Standard NPK (e.g. 10-10-10) at transplant and again at 4 weeks. Add compost if available."
        tips.append("Loamy soil is best for tobacco — maintain with crop rotation.")

    if score >= 70:
        rating = "Good"
        rating_ny = "Zabwino"
        color = "green"
    elif score >= 45:
        rating = "Medium"
        rating_ny = "Wapakati"
        color = "yellow"
    else:
        rating = "Poor"
        rating_ny = "Zosavuta"
        color = "red"

    return {
        "rating": rating,
        "rating_ny": rating_ny,
        "color": color,
        "score": score,
        "fertilizer_advice": fertilizer,
        "improvement_tips": tips,
    }
