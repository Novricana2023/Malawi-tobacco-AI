"""Simple rule-based yield estimation for smallholder tobacco."""

from __future__ import annotations

from typing import Any

STAGES = ["Nursery", "Transplanting", "Growing", "Ready to harvest"]

# Typical smallholder yield in kg per hectare (air-cured tobacco, Malawi)
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
) -> dict[str, Any]:
    """Estimate harvest in kg with simple adjustments."""
    hectares = max(0.01, min(hectares, 50.0))
    stage_mult = STAGE_MULTIPLIERS.get(stage, 0.5)
    soil_mult = SOIL_BONUS.get(soil_rating, 1.0)
    risk_mult = RISK_PENALTY.get(disease_risk, 1.0)

    projected = BASE_YIELD_KG_HA * hectares * stage_mult * soil_mult * risk_mult
    at_harvest = BASE_YIELD_KG_HA * hectares * soil_mult * risk_mult

    if stage == "Ready to harvest":
        message = "Field is near harvest. Check leaf maturity before cutting."
    elif stage == "Growing":
        message = "Main growth phase — keep soil moisture steady and watch for disease."
    elif stage == "Transplanting":
        message = "Young plants need water daily for first 2 weeks after transplant."
    else:
        message = "Nursery stage — protect seedlings from sun and pests."

    return {
        "current_estimate_kg": round(projected, 1),
        "harvest_potential_kg": round(at_harvest, 1),
        "hectares": hectares,
        "stage": stage,
        "message": message,
        "bags_estimate": round(at_harvest / 50, 1),  # ~50 kg per bale/bag rough estimate
    }
