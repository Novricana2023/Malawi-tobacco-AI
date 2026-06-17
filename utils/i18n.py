"""Bilingual labels for English and Chichewa."""

LABELS = {
    "app_title": ("Tobacco Farmer Assist Malawi", "Thandizo la Alimi a Fodya – Malawi"),
    "welcome": ("Welcome, Farmer!", "Moni, Mlimi!"),
    "farm_status": ("Today's Farm Status", "Mkhalidwe wa Munda Lero"),
    "disease_risk": ("Disease Risk", "Chiwopsezo cha Matenda"),
    "weather_risk": ("Weather Risk", "Chiwopsezo cha Nyengo"),
    "soil_risk": ("Soil Risk", "Chiwopsezo cha Dothi"),
    "good": ("Good", "Zabwino"),
    "medium": ("Medium", "Wapakati"),
    "poor": ("Poor", "Zosavuta"),
    "low": ("Low", "Zochepa"),
    "high": ("High", "Zakukulu"),
    "check_now": ("Check Now", "Onani Tsopano"),
    "run_analysis": ("Run Analysis", "Yambitsani Kusanthula"),
    "advisory_only": (
        "Advisory only — not a medical diagnosis.",
        "Chidziwitso chokha — si chitsimikizo cha matenda.",
    ),
    "good_harvest": ("Good harvest conditions", "Nthawi yabwino yokolola"),
    "hold_harvest": ("Hold harvest if prices are low", "Dikirani kukolola ngati mitengo ili pansi"),
    "field_size": ("Field size (hectares)", "Kukula kwa munda (ma-hectare)"),
    "crop_stage": ("Crop stage", "Gawo la zomera"),
    "farm_notes": ("Farm notes", "Zolemba za munda"),
    "estimated_yield": ("Estimated yield", "Zomwe mungathe kukolola"),
    "soil_type": ("Soil type", "Mtundu wa dothi"),
    "moisture": ("Moisture level", "Kuchuluka kwa madzi"),
    "upload_image": ("Upload leaf photo", "Ikani chithunzi cha tsamba"),
    "select_symptoms": ("Select symptoms", "Sankhani zizindikilo"),
    "what_to_do": ("What to do next", "Chomwe muyenera kuchita"),
    "severity": ("Severity", "Kukula kwa vuto"),
    "rain_warning": ("Rain warning", "Chenjezo la mvula"),
    "heat_warning": ("Heat stress warning", "Chenjezo la kutentha"),
    "market_prices": ("Market prices", "Mitengo ya msika"),
    "about": ("About this tool", "Za chida ichi"),
    "chat_title": ("Farmer Chat", "Kukambirana ndi Mlimi"),
    "chat_welcome": (
        "Hello! I'm your tobacco farming companion. I can answer all your questions about tobacco farming.",
        "Mulibwanji! Ndine bwenzi lanu la alimi a fodya. Nditha kuyankha mafunso anu onse okhudza fodya.",
    ),
    "chat_subtitle": (
        "Ask questions in English or Chichewa",
        "Funsani m'Chingerezi kapena Chichewa",
    ),
    "chat_placeholder": (
        "Type your question here…",
        "Lembani funso lanu apa…",
    ),
    "chat_send": ("Send", "Tumizani"),
    "sample_healthy": ("Healthy leaf example", "Chitsanzo cha tsamba lathu"),
    "sample_diseased": ("Diseased leaf example", "Chitsanzo cha tsamba lodwala"),
}

RISK_LEVELS = {
    "green": ("All clear", "Zili bwino"),
    "yellow": ("Watch closely", "Onani mosamala"),
    "red": ("Take action", "Chitani kanthu tsopano"),
}


def t(key: str, lang: str = "en") -> str:
    """Return label in requested language ('en' or 'ny' for Chichewa)."""
    entry = LABELS.get(key, (key, key))
    return entry[1] if lang == "ny" else entry[0]
