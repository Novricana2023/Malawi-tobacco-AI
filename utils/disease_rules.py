"""Rule-based tobacco leaf disease classification for smallholder farmers."""

from __future__ import annotations

from io import BytesIO
from typing import Any

# Tobacco diseases relevant to Malawi smallholders
TOBACCO_DISEASES: dict[str, dict[str, Any]] = {
    "Tobacco Mosaic Virus": {
        "symptoms": [
            "Mottled green and yellow patches",
            "Curled or twisted leaves",
            "Stunted plant growth",
            "Light and dark green mosaic pattern",
        ],
        "severity_factors": {"stunted", "mosaic", "curled"},
        "advice": {
            "low": "Remove affected leaves. Wash hands before touching other plants.",
            "medium": "Remove sick plants. Do not share tools between fields.",
            "high": "Remove and burn affected plants. Plant resistant varieties next season.",
        },
        "chichewa": "Matenda a Mozaiki wa Fodya",
    },
    "Black Shank": {
        "symptoms": [
            "Black lesions on stem near soil",
            "Wilting leaves in hot sun",
            "Yellowing lower leaves",
            "Root rot or dark stem base",
        ],
        "severity_factors": {"wilting", "stem_black", "root_rot"},
        "advice": {
            "low": "Improve drainage. Avoid waterlogging in the field.",
            "medium": "Apply recommended fungicide. Rotate crops next season.",
            "high": "Remove infected plants immediately. Do not replant tobacco here for 2 years.",
        },
        "chichewa": "Black Shank",
    },
    "Blue Mold": {
        "symptoms": [
            "Blue-gray fuzzy mold on leaf underside",
            "Yellow spots on upper leaf surface",
            "Rapid spread in cool wet weather",
            "Large irregular lesions",
        ],
        "severity_factors": {"blue_mold", "yellow_spots", "rapid_spread"},
        "advice": {
            "low": "Increase air flow between plants. Reduce leaf wetness.",
            "medium": "Apply fungicide early. Remove heavily infected leaves.",
            "high": "Spray immediately and remove worst plants. Avoid field work when leaves are wet.",
        },
        "chichewa": "Mould Wabuluu",
    },
    "Leaf Spot": {
        "symptoms": [
            "Small brown or tan circular spots",
            "Spots with dark borders",
            "Spots merge into larger patches",
            "Premature leaf drop",
        ],
        "severity_factors": {"brown_spots", "spot_merge", "leaf_drop"},
        "advice": {
            "low": "Remove spotted leaves. Keep field clean of old leaves.",
            "medium": "Spray copper-based fungicide. Space plants for air flow.",
            "high": "Spray weekly until controlled. Destroy severely affected plants.",
        },
        "chichewa": "Malo Owala pa Tsamba",
    },
    "Bacterial Wilt": {
        "symptoms": [
            "Sudden wilting of whole plant",
            "Brown streaks inside stem",
            "Sticky ooze from cut stem",
            "Leaves stay green then wilt rapidly",
        ],
        "severity_factors": {"sudden_wilt", "stem_streak", "sticky_ooze"},
        "advice": {
            "low": "Check irrigation. Avoid wounding plants during field work.",
            "medium": "Remove wilted plants. Disinfect tools with bleach solution.",
            "high": "Uproot and destroy all infected plants. Do not use that field for tobacco.",
        },
        "chichewa": "Kufota kwa Bakiteriya",
    },
    "Healthy Leaf": {
        "symptoms": [],
        "severity_factors": set(),
        "advice": {
            "low": "Leaf looks healthy. Continue regular field checks twice a week.",
            "medium": "Leaf looks mostly fine. Monitor for early signs of disease.",
            "high": "Continue monitoring. No urgent action needed.",
        },
        "chichewa": "Tsamba Lathu",
    },
}

# Symptom options shown in UI → internal keys
SYMPTOM_MAP: dict[str, str] = {
    "Yellow or mottled patches": "mosaic",
    "Curled or twisted leaves": "curled",
    "Stunted growth": "stunted",
    "Black stem near soil": "stem_black",
    "Wilting in hot sun": "wilting",
    "Root rot / dark stem base": "root_rot",
    "Blue-gray mold underneath": "blue_mold",
    "Yellow spots on leaf top": "yellow_spots",
    "Spreading fast after rain": "rapid_spread",
    "Small brown circular spots": "brown_spots",
    "Spots merging together": "spot_merge",
    "Leaves falling early": "leaf_drop",
    "Sudden whole-plant wilting": "sudden_wilt",
    "Brown streaks inside stem": "stem_streak",
    "Sticky ooze from stem": "sticky_ooze",
}


def _severity_from_score(score: int) -> str:
    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"


def classify_by_symptoms(selected_symptoms: list[str]) -> dict[str, Any]:
    """Match farmer-selected symptoms to the most likely tobacco disease."""
    if not selected_symptoms:
        return {
            "disease": "Unknown",
            "severity": "low",
            "confidence": 0.0,
            "advice": "Select symptoms or upload a leaf photo for guidance.",
            "chichewa_name": "Sizindikiridwa",
        }

    internal = {SYMPTOM_MAP[s] for s in selected_symptoms if s in SYMPTOM_MAP}
    best_disease = "Leaf Spot"
    best_score = 0

    for name, info in TOBACCO_DISEASES.items():
        if name == "Healthy Leaf":
            continue
        overlap = len(internal & info["severity_factors"])
        if overlap > best_score:
            best_score = overlap
            best_disease = name

    if best_score == 0:
        best_disease = "Leaf Spot"
        best_score = 1

    severity = _severity_from_score(best_score)
    info = TOBACCO_DISEASES[best_disease]
    confidence = min(0.95, 0.35 + best_score * 0.15)

    return {
        "disease": best_disease,
        "severity": severity,
        "confidence": round(confidence, 2),
        "advice": info["advice"][severity],
        "chichewa_name": info["chichewa"],
        "matched_symptoms": best_score,
    }


def analyze_image_simple(image_bytes: bytes) -> dict[str, Any]:
    """
    Lightweight image heuristic when no ML model is available.
    Uses color distribution — advisory only, not a diagnosis.
    """
    try:
        from PIL import Image
        import numpy as np

        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((256, 256))
        arr = np.array(img, dtype=float)

        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        total = max(r.mean() + g.mean() + b.mean(), 1.0)

        green_ratio = g.mean() / total
        yellow_mask = (r > 150) & (g > 130) & (b < 100)
        brown_mask = (r > 80) & (g < 100) & (b < 80)
        dark_mask = (r < 60) & (g < 60) & (b < 60)

        yellow_pct = yellow_mask.mean()
        brown_pct = brown_mask.mean()
        dark_pct = dark_mask.mean()

        if yellow_pct > 0.12 and green_ratio < 0.38:
            symptoms = ["Yellow or mottled patches", "Curled or twisted leaves"]
        elif dark_pct > 0.08:
            symptoms = ["Black stem near soil", "Root rot / dark stem base"]
        elif brown_pct > 0.10:
            symptoms = ["Small brown circular spots", "Spots merging together"]
        elif yellow_pct > 0.06:
            symptoms = ["Yellow spots on leaf top", "Blue-gray mold underneath"]
        elif green_ratio > 0.40 and yellow_pct < 0.05 and brown_pct < 0.05:
            result = classify_by_symptoms([])
            result.update(
                {
                    "disease": "Healthy Leaf",
                    "severity": "low",
                    "confidence": 0.55,
                    "advice": TOBACCO_DISEASES["Healthy Leaf"]["advice"]["low"],
                    "chichewa_name": TOBACCO_DISEASES["Healthy Leaf"]["chichewa"],
                    "method": "image_heuristic",
                }
            )
            return result
        else:
            symptoms = ["Small brown circular spots"]

        result = classify_by_symptoms(symptoms)
        result["method"] = "image_heuristic"
        result["image_signals"] = {
            "green_ratio": round(green_ratio, 2),
            "yellow_pct": round(yellow_pct, 2),
            "brown_pct": round(brown_pct, 2),
        }
        return result

    except Exception:
        return {
            "disease": "Unknown",
            "severity": "low",
            "confidence": 0.0,
            "advice": "Could not read image. Please select symptoms manually.",
            "chichewa_name": "Sizindikiridwa",
            "method": "error",
        }


def get_all_symptom_options() -> list[str]:
    return list(SYMPTOM_MAP.keys())
