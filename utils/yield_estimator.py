"""Simple rule-based yield estimation for smallholder tobacco."""

from __future__ import annotations

from typing import Any

from utils.i18n import STAGE_KEYS, stage_label, t

STAGES = STAGE_KEYS
BASE_YIELD_KG_HA = 1200

STAGE_MULTIPLIERS = {
    "Nursery": 0.05,
    "Transplanting": 0.25,
    "Growing": 0.70,
    "Ready to harvest": 1.0,
}

SOIL_BONUS = {"Good": 1.15, "Medium": 1.0, "Poor": 0.75}
RISK_PENALTY = {"green": 1.0, "yellow": 0.85, "red": 0.65}


def estimate_yield(
    hectares: float,
    stage: str,
    soil_rating: str = "Medium",
    disease_risk: str = "green",
    lang: str = "en",
) -> dict[str, Any]:
    hectares = max(0.01, min(hectares, 50.0))
    stage_mult = STAGE_MULTIPLIERS.get(stage, 0.5)
    soil_mult = SOIL_BONUS.get(soil_rating, 1.0)
    risk_mult = RISK_PENALTY.get(disease_risk, 1.0)

    projected = BASE_YIELD_KG_HA * hectares * stage_mult * soil_mult * risk_mult
    at_harvest = BASE_YIELD_KG_HA * hectares * soil_mult * risk_mult

    if stage == "Ready to harvest":
        message = t("yield_harvest", lang)
    elif stage == "Growing":
        message = t("yield_growing", lang)
    elif stage == "Transplanting":
        message = t("yield_transplant", lang)
    else:
        message = t("yield_nursery", lang)

    return {
        "current_estimate_kg": round(projected, 1),
        "harvest_potential_kg": round(at_harvest, 1),
        "hectares": hectares,
        "stage": stage_label(stage, lang),
        "message": message,
        "bags_estimate": round(at_harvest / 50, 1),
    }
