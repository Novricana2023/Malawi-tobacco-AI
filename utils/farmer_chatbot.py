"""Offline farmer chatbot — English and Chichewa, no API required."""

from __future__ import annotations

import re
from typing import Any

# Keyword → response pairs (English, Chichewa)
FAQ: list[dict[str, Any]] = [
    {
        "keywords_en": ["hello", "hi", "moni", "help", "start", "companion"],
        "keywords_ny": ["moni", "mulibwanji", "mbale", "thandizo", "dziwani", "kuyamba", "bwenzi"],
        "en": "Hello! I'm your tobacco farming companion. I can answer all your questions about tobacco farming.",
        "ny": "Mulibwanji! Ndine bwenzi lanu la alimi a fodya. Nditha kuyankha mafunso anu onse okhudza fodya.",
    },
    {
        "keywords_en": ["disease", "sick", "leaf", "spot", "virus", "mold", "wilt", "mosaic"],
        "keywords_ny": ["matenda", "odwala", "tsamba", "malo", "mozaiki", "kufota"],
        "en": "For leaf disease: go to Leaf Disease Checker. Upload a photo or select symptoms. Remove sick leaves early and wash hands between plants.",
        "ny": "Pa matenda a tsamba: pitani ku Leaf Disease Checker. Ikani chithunzi kapena sankhani zizindikilo. Chotsani masamba odwala msanga ndipo samani manja pakati pa zomera.",
    },
    {
        "keywords_en": ["black shank", "stem", "black stem"],
        "keywords_ny": ["black shank", "mtengo", "wakuda"],
        "en": "Black Shank: black lesions on stem near soil, wilting in sun. Improve drainage, remove infected plants, rotate crops for 2 years.",
        "ny": "Black Shank: malo akuda pa mtengo pafupi ndi dothi, kufota mu dzuwa. Imitsani kuthira madzi, chotsani zomera zodwala, sinjani zomera kwa zaka 2.",
    },
    {
        "keywords_en": ["soil", "ph", "fertilizer", "manure", "compost", "clay", "sandy", "loamy"],
        "keywords_ny": ["dothi", "manyowa", "pH", "feteleza", "manyowa", "dothi lotopa", "dothi la mchenga"],
        "en": "Tobacco likes loamy soil, pH 5.5–6.5, medium moisture. Sandy soil needs compost. Clay needs ridges for drainage. Check Soil Check page.",
        "ny": "Fodya imakonda dothi la loamy, pH 5.5–6.5, madzi wapakati. Dothi la mchenga limafuna manyowa. Dothi lotopa limafuna mipiri ya kuthira madzi. Onani tsamba la Soil Check.",
    },
    {
        "keywords_en": ["rain", "weather", "heat", "sun", "dry", "wet", "irrigation", "water"],
        "keywords_ny": ["mvula", "nyengo", "kutentha", "dzuwa", "kukauma", "kunyowa", "madzi"],
        "en": "Do not dry tobacco on rainy days. Water early morning in heat. Check Weather page for today's advice.",
        "ny": "Musawopsye fodya masiku amvula. Phirimitsani madzi mmamawa akale pamakutu. Onani tsamba la Weather kuti muone upangiri wa lero.",
    },
    {
        "keywords_en": ["harvest", "pick", "cut", "cure", "dry", "kolola"],
        "keywords_ny": ["kukolola", "kudula", "kuwopsya", "kukolola fodya"],
        "en": "Harvest when leaves turn light green to yellow. Cure in well-ventilated barn. Do not dry when rain is coming.",
        "ny": "Kololani pamene masamba asintha kukhala obiriwira kapena a mtundu wa yellow. Wopsani m'bwalo lomwe lili ndi mphepo. Musawopsye ngati mvula ikubwera.",
    },
    {
        "keywords_en": ["price", "market", "sell", "buy", "auction", "mwk"],
        "keywords_ny": ["mitengo", "msika", "kugulitsa", "kugula", "auction"],
        "en": "Check Market Price Guide page. If prices are high and crop is ready, consider selling. If low, hold if crop can wait.",
        "ny": "Onani tsamba la Market Price Guide. Ngati mitengo ikwera ndipo fodya yakonzeka, ganizirani kugulitsa. Ngati ili pansi, dikirani ngati fodya ingadikire.",
    },
    {
        "keywords_en": ["yield", "hectare", "field", "how much", "kg"],
        "keywords_ny": ["kukolola", "hectare", "munda", "kuchuluka"],
        "en": "Smallholders often get 800–1500 kg per hectare. Use My Tobacco Field page to estimate based on your field size and crop stage.",
        "ny": "Alimi angathe kukolola kg 800–1500 pa hectare. Gwiritsani ntchito tsamba la My Tobacco Field kuyeza ndi kukula kwa munda ndi gawo la zomera.",
    },
    {
        "keywords_en": ["nursery", "seedling", "transplant"],
        "keywords_ny": ["nursery", "zomera zazing'ono", "kusenza"],
        "en": "Nursery: protect from sun and pests. Transplant when seedlings are 15–20 cm. Water daily for first 2 weeks after transplant.",
        "ny": "Nursery: tetezani ku dzuwa ndi tiziwala. Sinani pamene zomera zili 15–20 cm. Phirimitsani madzi tsiku ndi tsiku kwa masabata 2 pambuyo pa kusenza.",
    },
    {
        "keywords_en": ["extension", "advisor", "office", "expert"],
        "keywords_ny": ["othandizira", "ofesi", "katswiri"],
        "en": "Visit your local Agriculture Extension office for free soil testing and expert advice. This app is advisory only.",
        "ny": "Pitani ku Agriculture Extension office yanu kuti mupeze mayeso a dothi kwaulere ndi upangiri wochokera kwa akatswiri. Chida ichi ndi chidziwitso chokha.",
    },
]

DEFAULT = {
    "en": "I did not understand. Try asking about: disease, soil, weather, harvest, or market prices. Or type 'help'.",
    "ny": "Sinamvetse. Yesani kufunsa za: matenda, dothi, nyengo, kukolola, kapena mitengo. Kapena lembani 'thandizo'.",
}

QUICK_PROMPTS = {
    "en": [
        "My leaf has yellow spots",
        "Is sandy soil good for tobacco?",
        "Can I dry tobacco today?",
        "When should I harvest?",
    ],
    "ny": [
        "Tsamba langa lili ndi malo a yellow",
        "Kodi dothi la mchenga ndi labwino pa fodya?",
        "Kodi ndingawopsye fodya lero?",
        "Ndi nthawi yanji yokolola?",
    ],
}


def _match_faq(text: str, lang: str) -> str | None:
    text_lower = text.lower()
    for item in FAQ:
        keys = item["keywords_ny"] if lang == "ny" else item["keywords_en"]
        for kw in keys:
            if kw.lower() in text_lower:
                return item[lang]
    return None


def get_offline_response(prompt: str, language: str = "en") -> str:
    """
    Offline rule-based chatbot for farmers.
    language: 'en' or 'ny' (Chichewa)
    """
    if not prompt or not prompt.strip():
        return DEFAULT.get(language, DEFAULT["en"])

    text = prompt.strip()
    lang = "ny" if language == "ny" else "en"

    # Direct help command
    if re.search(r"\b(help|thandizo|dziwani)\b", text, re.I):
        return FAQ[0][lang]

    matched = _match_faq(text, lang)
    if matched:
        return matched

    # Try other language keywords as fallback
    other = "en" if lang == "ny" else "ny"
    matched = _match_faq(text, other)
    if matched:
        return matched

    return DEFAULT[lang]


# Backwards-compatible alias
get_chatbot_response = get_offline_response
