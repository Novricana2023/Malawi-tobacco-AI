"""Soil suitability evaluation for tobacco in Malawi."""

from __future__ import annotations

from typing import Any

from utils.i18n import SOIL_KEYS, MOISTURE_KEYS, rating_label, soil_label, t

SOIL_TYPES = SOIL_KEYS
MOISTURE_LEVELS = MOISTURE_KEYS


def evaluate_soil(
    soil_type: str,
    ph: float | None,
    moisture: str,
    lang: str = "en",
) -> dict[str, Any]:
    score = 50
    tips: list[str] = []
    fertilizer: str

    soil_scores = {"Loamy": 25, "Sandy": 10, "Clay": -5}
    score += soil_scores.get(soil_type, 0)

    if ph is not None:
        if 5.5 <= ph <= 6.5:
            score += 20
            tips.append(
                "pH ili mkati mwa 5.5–6.5 — labwino pa fodya."
                if lang == "ny"
                else "pH is in the ideal range for tobacco (5.5–6.5)."
            )
        elif 5.0 <= ph < 5.5 or 6.5 < ph <= 7.0:
            score += 5
            tips.append(
                "pH yavomerezeka koma si yabwino kwambiri. Pitani ku extension kuti mupeze mayeso."
                if lang == "ny"
                else "pH is acceptable but not ideal. Consider soil testing at extension office."
            )
        else:
            score -= 15
            tips.append(
                "pH silili bwino. Funsani akatswiri za lime kapena sulfur."
                if lang == "ny"
                else "pH is outside ideal range. Lime or sulfur may be needed — ask extension worker."
            )
    else:
        tips.append(
            "Simudziwa pH — pitani ku Agriculture Extension kuti mupeze mayeso kwaulere."
            if lang == "ny"
            else "pH unknown — visit your agriculture extension office for free soil testing."
        )

    moisture_scores = {"Dry": -10, "Medium": 15, "Wet": -20}
    score += moisture_scores.get(moisture, 0)

    if moisture == "Dry":
        tips.append(
            "Phirimitsani madzi mmamawa. Ikani manyowa mozungulira zomera."
            if lang == "ny"
            else "Irrigate lightly in early morning. Mulch around plants to keep moisture."
        )
    elif moisture == "Wet":
        tips.append(
            "Imitsani kuthira madzi ndi mipiri. Musagwire ntchito m'munda woyedwa."
            if lang == "ny"
            else "Improve drainage with ridges. Avoid working field when waterlogged."
        )
    else:
        tips.append(
            "Madzi ali bwino. Pitilizani kuyang'ana mmamawa."
            if lang == "ny"
            else "Moisture level is good. Maintain with regular morning checks."
        )

    if soil_type == "Sandy":
        fertilizer = (
            "Ikani manyowa kapena manyowa obvala musanadzaze. Gawani feteleza wa NPK m' magawo 2."
            if lang == "ny"
            else "Apply compost or well-rotted manure before transplanting. Split NPK fertilizer in 2 doses."
        )
        tips.append(
            "Dothi la mchenga limataya chuma msanga — onjezerani zinthu za organic nyengo iliyonse."
            if lang == "ny"
            else "Sandy soil loses nutrients fast — add organic matter every season."
        )
    elif soil_type == "Clay":
        fertilizer = (
            "Gwiritsani NPK yochepa. Onjezerani mchenga ndi manyowa."
            if lang == "ny"
            else "Use lighter NPK dose. Add sand and compost to improve structure."
        )
        tips.append(
            "Dothi lotopa limasunga madzi — limani pa mipiri kuti mizu asaphe."
            if lang == "ny"
            else "Clay holds water — plant on ridges to prevent root rot."
        )
    else:
        fertilizer = (
            "NPK (mwachitsanzo 10-10-10) pa kusenza ndiponso m' masabata 4. Onjezerani manyowa."
            if lang == "ny"
            else "Standard NPK (e.g. 10-10-10) at transplant and again at 4 weeks. Add compost if available."
        )
        tips.append(
            "Dothi la loamy ndi labwino pa fodya — sungani ndi kusintha zomera."
            if lang == "ny"
            else "Loamy soil is best for tobacco — maintain with crop rotation."
        )

    if score >= 70:
        rating, color = "Good", "green"
    elif score >= 45:
        rating, color = "Medium", "yellow"
    else:
        rating, color = "Poor", "red"

    return {
        "rating_key": rating,
        "rating": rating_label(rating, lang),
        "color": color,
        "score": score,
        "fertilizer_advice": fertilizer,
        "improvement_tips": tips,
    }
