"""Rule-based tobacco leaf disease classification for smallholder farmers."""

from __future__ import annotations

from io import BytesIO
from typing import Any

from utils.i18n import t

# internal_key, English label, Chichewa label
SYMPTOM_ENTRIES: list[tuple[str, str, str]] = [
    ("mosaic", "Yellow or mottled patches", "Malo a green ndi yellow"),
    ("curled", "Curled or twisted leaves", "Masamba obvala kapena ovunda"),
    ("stunted", "Stunted growth", "Kukula kochepa"),
    ("stem_black", "Black stem near soil", "Mtengo wakuda pafupi ndi dothi"),
    ("wilting", "Wilting in hot sun", "Kufota mu dzuwa lotentha"),
    ("root_rot", "Root rot / dark stem base", "Mizu kufota / mtengo wakuda"),
    ("blue_mold", "Blue-gray mold underneath", "Mould wabuluu pansi pa tsamba"),
    ("yellow_spots", "Yellow spots on leaf top", "Malo a yellow pamwamba pa tsamba"),
    ("rapid_spread", "Spreading fast after rain", "Kufalikira msanga after mvula"),
    ("brown_spots", "Small brown circular spots", "Malo a brown ang'ono"),
    ("spot_merge", "Spots merging together", "Malo kuphatikiza"),
    ("leaf_drop", "Leaves falling early", "Masamba kugwa msanga"),
    ("sudden_wilt", "Sudden whole-plant wilting", "Kufota kwadzidzidzi kwa chomera"),
    ("stem_streak", "Brown streaks inside stem", "Mizere ya brown mkati mwa mtengo"),
    ("sticky_ooze", "Sticky ooze from stem", "Chinyezi chomata pa mtengo"),
]

TOBACCO_DISEASES: dict[str, dict[str, Any]] = {
    "Tobacco Mosaic Virus": {
        "severity_factors": {"stunted", "mosaic", "curled"},
        "en": "Tobacco Mosaic Virus",
        "ny": "Matenda a Mozaiki wa Fodya",
        "advice": {
            "low": "Remove affected leaves. Wash hands before touching other plants.",
            "medium": "Remove sick plants. Do not share tools between fields.",
            "high": "Remove and burn affected plants. Plant resistant varieties next season.",
        },
        "advice_ny": {
            "low": "Chotsani masamba odwala. Samani manja musanakhudze zomera zina.",
            "medium": "Chotsani zomera zodwala. Musagawane zipangizo pakati pa minda.",
            "high": "Chotsani ndipo mutenthe zomera zodwala. Dunani mtundu wolimba nyengo yotsatira.",
        },
    },
    "Black Shank": {
        "severity_factors": {"wilting", "stem_black", "root_rot"},
        "en": "Black Shank",
        "ny": "Black Shank",
        "advice": {
            "low": "Improve drainage. Avoid waterlogging in the field.",
            "medium": "Apply recommended fungicide. Rotate crops next season.",
            "high": "Remove infected plants immediately. Do not replant tobacco here for 2 years.",
        },
        "advice_ny": {
            "low": "Imitsani kuthira madzi. Musaziyese minda ndi madzi ambiri.",
            "medium": "Gwiritsani ntchito mankhwala a fungicide. Sinani zomera nyengo yotsatira.",
            "high": "Chotsani zomera msanga. Musadzazenso fodya pano kwa zaka 2.",
        },
    },
    "Blue Mold": {
        "severity_factors": {"blue_mold", "yellow_spots", "rapid_spread"},
        "en": "Blue Mold",
        "ny": "Mould Wabuluu",
        "advice": {
            "low": "Increase air flow between plants. Reduce leaf wetness.",
            "medium": "Apply fungicide early. Remove heavily infected leaves.",
            "high": "Spray immediately and remove worst plants. Avoid field work when leaves are wet.",
        },
        "advice_ny": {
            "low": "Pangani mphepo pakati pa zomera. Chepetsani kunyowa pa masamba.",
            "medium": "Giritsani fungicide msanga. Chotsani masamba odwala kwambiri.",
            "high": "Popera msanga ndipo chotsani zomera zovuta. Musagwire ntchito masamba akunyowa.",
        },
    },
    "Leaf Spot": {
        "severity_factors": {"brown_spots", "spot_merge", "leaf_drop"},
        "en": "Leaf Spot",
        "ny": "Malo Owala pa Tsamba",
        "advice": {
            "low": "Remove spotted leaves. Keep field clean of old leaves.",
            "medium": "Spray copper-based fungicide. Space plants for air flow.",
            "high": "Spray weekly until controlled. Destroy severely affected plants.",
        },
        "advice_ny": {
            "low": "Chotsani masamba okhala ndi malo. Sungani munda woyera.",
            "medium": "Popera mankhwala a copper. Sikani zomera kuti mphepo ipite.",
            "high": "Popera sabata ndi sabata mpaka zatheka. Chotsani zomera zodwala kwambiri.",
        },
    },
    "Bacterial Wilt": {
        "severity_factors": {"sudden_wilt", "stem_streak", "sticky_ooze"},
        "en": "Bacterial Wilt",
        "ny": "Kufota kwa Bakiteriya",
        "advice": {
            "low": "Check irrigation. Avoid wounding plants during field work.",
            "medium": "Remove wilted plants. Disinfect tools with bleach solution.",
            "high": "Uproot and destroy all infected plants. Do not use that field for tobacco.",
        },
        "advice_ny": {
            "low": "Onani kuthira madzi. Musamavulaze zomera mukamagwira ntchito.",
            "medium": "Chotsani zomera zofota. Samitsani zipangizo ndi bleach.",
            "high": "Dulani ndipo chotsani zomera zonse. Musadzazenso fodya m'mundamo.",
        },
    },
    "Healthy Leaf": {
        "severity_factors": set(),
        "en": "Healthy Leaf",
        "ny": "Tsamba Lathu",
        "advice": {
            "low": "Leaf looks healthy. Continue regular field checks twice a week.",
            "medium": "Leaf looks mostly fine. Monitor for early signs of disease.",
            "high": "Continue monitoring. No urgent action needed.",
        },
        "advice_ny": {
            "low": "Tsamba likuwoneka lathu. Pitilizani kuyang'ana munda kawiri pa sabata.",
            "medium": "Tsamba likuwoneka labwino. Samalitsani zizindikilo za matenda.",
            "high": "Pitilizani kuyang'ana. Palibe chofunika msanga.",
        },
    },
}


def _label_to_key(label: str, lang: str) -> str | None:
    for key, en, ny in SYMPTOM_ENTRIES:
        if label == (ny if lang == "ny" else en):
            return key
    return None


def get_all_symptom_options(lang: str = "en") -> list[str]:
    return [ny if lang == "ny" else en for _, en, ny in SYMPTOM_ENTRIES]


def _localize_result(disease_key: str, severity: str, confidence: float, lang: str, **extra) -> dict[str, Any]:
    info = TOBACCO_DISEASES[disease_key]
    advice_key = "advice_ny" if lang == "ny" else "advice"
    name_key = "ny" if lang == "ny" else "en"
    return {
        "disease": info[name_key],
        "severity": severity,
        "confidence": confidence,
        "advice": info[advice_key][severity],
        **extra,
    }


def classify_by_symptoms(selected_symptoms: list[str], lang: str = "en") -> dict[str, Any]:
    if not selected_symptoms:
        return {
            "disease": t("unknown", lang),
            "severity": "low",
            "confidence": 0.0,
            "advice": t("analyze_prompt", lang),
        }

    internal = {_label_to_key(s, lang) for s in selected_symptoms}
    internal.discard(None)

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
        best_score = 1

    severity = _severity_from_score(best_score)
    confidence = round(min(0.95, 0.35 + best_score * 0.15), 2)
    return _localize_result(best_disease, severity, confidence, lang, matched_symptoms=best_score)


def en_symptoms_for_lang(en_labels: list[str], lang: str) -> list[str]:
    en_list = get_all_symptom_options("en")
    ny_list = get_all_symptom_options("ny")
    out = []
    for s in en_labels:
        if s in en_list:
            idx = en_list.index(s)
            out.append(ny_list[idx] if lang == "ny" else s)
    return out


def _severity_from_score(score: int) -> str:
    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"


def analyze_image_simple(image_bytes: bytes, lang: str = "en") -> dict[str, Any]:
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

        en_symptoms: list[str]
        if yellow_pct > 0.12 and green_ratio < 0.38:
            en_symptoms = ["Yellow or mottled patches", "Curled or twisted leaves"]
        elif dark_pct > 0.08:
            en_symptoms = ["Black stem near soil", "Root rot / dark stem base"]
        elif brown_pct > 0.10:
            en_symptoms = ["Small brown circular spots", "Spots merging together"]
        elif yellow_pct > 0.06:
            en_symptoms = ["Yellow spots on leaf top", "Blue-gray mold underneath"]
        elif green_ratio > 0.40 and yellow_pct < 0.05 and brown_pct < 0.05:
            result = _localize_result("Healthy Leaf", "low", 0.55, lang, method="image_heuristic")
            return result
        else:
            en_symptoms = ["Small brown circular spots"]

        if lang == "ny":
            symptoms = en_symptoms_for_lang(en_symptoms, lang)
        else:
            symptoms = en_symptoms

        result = classify_by_symptoms(symptoms, lang)
        result["method"] = "image_heuristic"
        return result

    except Exception:
        return {
            "disease": t("unknown", lang),
            "severity": "low",
            "confidence": 0.0,
            "advice": t("analyze_prompt", lang),
            "method": "error",
        }
