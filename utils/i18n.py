"""English and Chichewa labels — one language at a time based on user selection."""

from __future__ import annotations

LABELS: dict[str, tuple[str, str]] = {
    # Cover & home
    "cover_title": ("Mlimi Smart Assistant", "Mlimi Smart Assistant"),
    "cover_subtitle": (
        "Smart support for smallholder tobacco farmers in Malawi",
        "Thandizo lanzeru kwa alimi aang'ono a fodya ku Malawi",
    ),
    "cover_badge": ("Malawi · Tobacco · Smart Farming", "Malawi · Fodya · Limi Lanzeru"),
    "welcome": ("Welcome, Farmer!", "Moni, Mlimi!"),
    "sidebar_title": ("Farmer Assist Malawi", "Thandizo la Alimi – Malawi"),
    "sidebar_caption": (
        "Made for smallholder tobacco farmers in Malawi",
        "Zopangidwa kwa alimi aang'ono a fodya ku Malawi",
    ),
    "lang_label": ("Language", "Chilankhulo"),
    "farm_status": ("Today's Farm Status", "Mkhalidwe wa Munda Lero"),
    "disease_risk": ("Disease Risk", "Chiwopsezo cha Matenda"),
    "weather_risk": ("Weather Risk", "Chiwopsezo cha Nyengo"),
    "soil_risk": ("Soil Risk", "Chiwopsezo cha Dothi"),
    "estimated_yield": ("Estimated yield", "Zomwe mungathe kukolola"),
    "field_size_label": ("Field size", "Kukula kwa munda"),
    "temperature": ("Temperature", "Kutentha"),
    "market_prices": ("Market prices", "Mitengo ya msika"),
    "bags": ("bags", "matumba"),
    "quick_actions": ("Quick Actions", "Zochita Msanga"),
    "btn_disease": ("Check Leaf Disease", "Onani Matenda a Tsamba"),
    "btn_soil": ("Check Soil", "Onani Dothi"),
    "btn_weather": ("Weather Advice", "Upangiri wa Nyengo"),
    "weather_check_warning": (
        "Check weather page before field work or drying tobacco.",
        "Onani tsamba la nyengo musanachite ntchito m'munda kapena kuwopsya fodya.",
    ),
    "advisory_only": (
        "Advisory only — not a medical diagnosis.",
        "Chidziwitso chokha — si chitsimikizo cha matenda.",
    ),
    "good_harvest": ("Good harvest conditions", "Nthawi yabwino yokolola"),
    "latest_disease": ("Latest Disease Check", "Kusanthula Kwathu kwa Matenda"),
    "severity_label": ("Severity", "Kukula kwa vuto"),
    "harvest_caption": ("Harvest season — smallholder tobacco", "Kukolola — fodya ya alimi aang'ono"),
    "sample_healthy": ("Healthy leaf example", "Chitsanzo cha tsamba lathu"),
    "sample_diseased": ("Diseased leaf example", "Chitsanzo cha tsamba lodwala"),
    # Chat
    "chat_title": ("Farmer Chat", "Kukambirana ndi Mlimi"),
    "chat_subtitle": ("Ask your farming questions here", "Funsani mafunso anu okhudza limi apa"),
    "chat_welcome": (
        "Hello! I'm your tobacco farming companion. I can answer all your questions about tobacco farming.",
        "Mulibwanji! Ndine bwenzi lanu la alimi a fodya. Nditha kuyankha mafunso anu onse okhudza fodya.",
    ),
    "chat_placeholder": ("Type your question here…", "Lembani funso lanu apa…"),
    "chat_quick": ("Quick questions", "Mafunso msanga"),
    "chat_clear": ("Clear chat", "Chotsani macheza"),
    "chat_openai_on": ("Smart answers enabled", "Mayankho anzeru akutheka"),
    "chat_openai_off": ("Offline mode — basic answers only", "Popanda intaneti — mayankho osavuta okha"),
    # Field page
    "page_field": ("My Tobacco Field", "Munda Wanga wa Fodya"),
    "field_size": ("Field size (hectares)", "Kukula kwa munda (ma-hectare)"),
    "crop_stage": ("Crop stage", "Gawo la zomera"),
    "farm_notes": ("Farm notes", "Zolemba za munda"),
    "yield_estimate": ("Yield Estimate", "Kuyeza Kukolola"),
    "btn_calculate": ("Calculate Yield", "Calculate Kukolola"),
    "btn_save": ("Save Field Info", "Sungani Zambiri za Munda"),
    "saved_ok": ("Field information saved!", "Zambiri za munda zasungidwa!"),
    "current_estimate": ("Current season estimate", "Kuyeza kwa nyengo ino"),
    "harvest_potential": ("Potential at harvest", "Zomwe mungathe kukolola"),
    "approx_bags": ("Approx. bags (~50 kg)", "Matumba (~50 kg)"),
    "notes_placeholder": (
        "e.g. Transplanted on 15 Nov, north corner has wet soil…",
        "mwachitsanzo: Zadzazidwa pa 15 Nov, kum'mwera kuli ndi dothi loyedwa…",
    ),
    # Stages
    "stage_Nursery": ("Nursery", "Nursery"),
    "stage_Transplanting": ("Transplanting", "Kusenza"),
    "stage_Growing": ("Growing", "Kukula"),
    "stage_Ready to harvest": ("Ready to harvest", "Zakonzeka kukololwa"),
    # Disease page
    "page_disease": ("Leaf Disease Checker", "Kuyang'ana Matenda a Tsamba"),
    "compare_leaves": ("Compare your leaf with these examples", "Fananitsani tsamba lanu ndi zitsanzo izi"),
    "tab_upload": ("Upload Photo", "Ikani Chithunzi"),
    "tab_symptoms": ("Select Symptoms", "Sankhani Zizindikilo"),
    "upload_help": ("Take a clear photo of the affected leaf in daylight.", "Jambitsani chithunzi chooneka bwino cha tsamba lodwala masana."),
    "uploaded_leaf": ("Uploaded leaf", "Tsamba lomwe mwadzaza"),
    "btn_analyze": ("Analyze Photo", "Santhani Chithunzi"),
    "btn_check_symptoms": ("Check Symptoms", "Onani Zizindikilo"),
    "symptoms_help": ("Choose all signs you see on the plant.", "Sankhani zizindikilo zonse zomwe mukuona pa chomera."),
    "results": ("Results", "Zotsatira"),
    "likely_issue": ("Likely issue", "Chomwe chingakhale"),
    "confidence": ("Confidence", "Kutsimikizika"),
    "unknown": ("Unknown", "Sizindikiridwa"),
    "analyze_prompt": ("Upload a photo or select symptoms, then click Analyze.", "Ikani chithunzi kapena sankhani zizindikilo, kenako dinani Sanjani."),
    "image_heuristic_note": (
        "Analysis used simple image colors — also check symptoms manually.",
        "Kusanthula kudagwiritsa ntchito mtundu wa chithunzi — onaninso zizindikilo ndi manja.",
    ),
    "what_to_do": ("What to do next", "Chomwe muyenera kuchita"),
    "sev_low": ("LOW", "ZOCHEPA"),
    "sev_medium": ("MEDIUM", "WAPAKATI"),
    "sev_high": ("HIGH", "ZAKUKULU"),
    # Soil page
    "page_soil": ("Soil Check", "Kuyang'ana Dothi"),
    "soil_caption": (
        "Important for Malawi smallholder fields",
        "Zofunika kwambiri kwa minda ya alimi aang'ono ku Malawi",
    ),
    "soil_image_caption": ("Tobacco field — soil health matters", "Munda wa fodya — thanzi la dothi ndi lofunika"),
    "know_ph": ("I know my soil pH", "Ndikudziwa pH ya dothi langa"),
    "ph_level": ("pH level", "Mulingo wa pH"),
    "ph_unknown_tip": (
        "pH unknown? Visit your extension office for free testing.",
        "Simudziwa pH? Pitani ku ofesi ya extension kuti mupeze mayeso kwaulere.",
    ),
    "btn_check_soil": ("Check Soil", "Onani Dothi"),
    "soil_rating": ("Rating", "Mlingo"),
    "fertilizer_advice": ("Fertilizer Advice", "Upangiri wa Feteleza"),
    "soil_tips": ("Soil Improvement Tips", "Malangizo Okonza Dothi"),
    "soil_enter_prompt": ("Enter your soil details and click Check Soil.", "Lembani zambiri za dothi lanu ndipo dinani Onani Dothi."),
    "soil_Loamy": ("Loamy", "Loamy (dothi labwino)"),
    "soil_Sandy": ("Sandy", "Mchenga"),
    "soil_Clay": ("Clay", "Dothi lotopa"),
    "moisture_Dry": ("Dry", "Kukauma"),
    "moisture_Medium": ("Medium", "Wapakati"),
    "moisture_Wet": ("Wet", "Kunyowa"),
    "rating_Good": ("Good", "Zabwino"),
    "rating_Medium": ("Medium", "Wapakati"),
    "rating_Poor": ("Poor", "Zosavuta"),
    # Weather page
    "page_weather": ("Weather & Farming Advice", "Nyengo ndi Upangiri wa Limi"),
    "weather_caption": ("Daily weather guidance for your field", "Upangiri wa nyengo tsiku ndi tsiku pa munda wanu"),
    "weather_manual": ("Enter weather manually (optional)", "Lembani nyengo ndi manja (ngati mukufuna)"),
    "btn_refresh_weather": ("Refresh weather data", "Tsitsani deta ya nyengo"),
    "btn_get_advice": ("Get Advice", "Pezani Upangiri"),
    "humidity": ("Humidity", "Kunyowa kwa mphepo"),
    "rain_today": ("Rain today", "Mvula lero"),
    "rain_forecast": ("Rain forecast", "Kuyembekezera kwa mvula"),
    "alerts": ("Alerts", "Chenjezo"),
    "farmer_advice": ("Farmer Advice", "Upangiri kwa Mlimi"),
    "alert_rain": ("Rain", "Mvula"),
    "alert_heat": ("Heat", "Kutentha"),
    "alert_disease": ("Disease", "Matenda"),
    # Market page
    "page_market": ("Market Price Guide", "Mitengo ya Msika"),
    "market_caption": (
        "Burley tobacco — sample prices for Lilongwe (MWK per kg)",
        "Fodya ya Burley — mitengo ya chitsanzo ya Lilongwe (MWK pa kg)",
    ),
    "market_image_caption": (
        "Harvest timing and market prices go together",
        "Nthawi yokolola ndi mitengo ya msika zimapangana",
    ),
    "current_price": ("Current price", "Mitengo lero"),
    "avg_4_week": ("4-week average", "Avareji wa masabata 4"),
    "weekly_change": ("Weekly change", "Kusintha kwa sabata"),
    "price_trend": ("Tobacco Price Trend", "Kukwera kwa Mitengo ya Fodya"),
    "price_axis": ("Price (MWK/kg)", "Mitengo (MWK/kg)"),
    "date_axis": ("Date", "Tsiku"),
    # Upload page
    "page_upload": ("Upload / Data Input", "Kutsitsa / Kuyika Zambiri"),
    "upload_caption": ("Works without uploads too", "Imagwira ntchito popanda kutsitsa zinthu"),
    "tab_leaf_images": ("Leaf Images", "Zithunzi za Masamba"),
    "tab_farm_records": ("Farm Records", "Zolemba za Munda"),
    "upload_example": ("Example: upload a photo like this", "Chitsanzo: ikani chithunzi chotere"),
    "upload_photos": ("Upload leaf photos", "Ikani zithunzi za masamba"),
    "btn_analyze_all": ("Analyze all uploads", "Santhani zithunzi zonse"),
    "record_intro": ("Simple farm record (saved this session only)", "Mbiri yosavuta ya munda (imasungidwa pano pano okha)"),
    "date": ("Date", "Tsiku"),
    "activity": ("Activity", "Ntchito"),
    "notes": ("Notes", "Zolemba"),
    "notes_ph": ("e.g. Applied fungicide on east field", "mwachitsanzo: Anaphirika mankhwala kummawa"),
    "btn_add_record": ("Add record", "Onjezerani mbiri"),
    "record_added": ("Record added!", "Mbiri yawonjezeredwa!"),
    "your_records": ("Your Records", "Mbiri Yanu"),
    "download_records": ("Download records (JSON)", "Tsitsani mbiri (JSON)"),
    "no_records": ("No records yet — add one above.", "Palibe mbiri pano — onjezerani pamwambapa."),
    "act_Planting": ("Planting", "Kufesa"),
    "act_Transplanting": ("Transplanting", "Kusenza"),
    "act_Spraying": ("Spraying", "Kupopera mankhwala"),
    "act_Harvesting": ("Harvesting", "Kukolola"),
    "act_Drying": ("Drying", "Kuwopsya"),
    "act_Other": ("Other", "Zina"),
    # About page
    "about": ("About this tool", "Za chida ichi"),
    "about_purpose_h": ("Purpose", "Cholinga"),
    "about_purpose": (
        "This tool helps **smallholder tobacco farmers in Malawi** make practical daily decisions about disease, soil, weather, yield, and market prices.",
        "Chida ichi chimathandiza **alimi aang'ono a fodya ku Malawi** kuchita zisankho zabwino tsiku ndi tsiku pa matenda, dothi, nyengo, kukolola, ndi mitengo ya msika.",
    ),
    "about_who_h": ("Who is it for?", "Akuti ndani?"),
    "about_who": (
        "Low-resource farmers — not large commercial estates. Designed for shared phones and slow connections.",
        "Alimi aang'ono — osati mafamu akulu. Zopangidwa kuti zigwire pa foni imodzi ndi intaneti yofoka.",
    ),
    "about_chat_h": ("Farmer Chat", "Kukambirana ndi Mlimi"),
    "about_chat": (
        "Use Farmer Chat on the home page to ask questions about disease, soil, weather, harvest, and prices.",
        "Gwiritsani ntchito Kukambirana ndi Mlimi patsamba loyamba kufunsa za matenda, dothi, nyengo, kukolola, ndi mitengo.",
    ),
    "about_important_h": ("Important", "Zofunika"),
    "about_important": (
        "All disease results are **advisory only**, not medical certainty. Visit your Agriculture Extension office for expert help.",
        "Zotsatira za matenda ndi **chidziwitso chokha**, si chitsimikizo. Pitani ku ofesi ya Agriculture Extension kuti mupeze thandizo la katswiri.",
    ),
    "about_footer": (
        "Built for Malawian smallholder farmers — simplicity over complexity.",
        "Zopangidwa kwa alimi aang'ono a fodya ku Malawi — kusavuta kuposa kuvuta.",
    ),
    "about_image_caption": (
        "Supporting smallholder farmers across Malawi",
        "Kuthandiza alimi aang'ono ku Malawi",
    ),
    # Yield messages
    "yield_harvest": ("Field is near harvest. Check leaf maturity before cutting.", "Munda wafika pafupi kukolola. Onani ngati masamba akonzeka musanadule."),
    "yield_growing": ("Main growth phase — keep soil moisture steady and watch for disease.", "Nthawi yokulira — sungani madzi ndipo samalitsani matenda."),
    "yield_transplant": ("Young plants need water daily for first 2 weeks after transplant.", "Zomera zazing'ono zimafuna madzi tsiku ndi tsiku kwa masabata 2 pambuyo pa kusenza."),
    "yield_nursery": ("Nursery stage — protect seedlings from sun and pests.", "Gawo la nursery — tetezani zomera ku dzuwa ndi tiziwala."),
    # Location
    "location": ("Central Region, Malawi", "Central Region, Malawi"),
}

STAGE_KEYS = ["Nursery", "Transplanting", "Growing", "Ready to harvest"]
SOIL_KEYS = ["Loamy", "Sandy", "Clay"]
MOISTURE_KEYS = ["Dry", "Medium", "Wet"]
ACTIVITY_KEYS = ["Planting", "Transplanting", "Spraying", "Harvesting", "Drying", "Other"]


def t(key: str, lang: str = "en") -> str:
    entry = LABELS.get(key, (key, key))
    return entry[1] if lang == "ny" else entry[0]


def stage_label(stage: str, lang: str) -> str:
    return t(f"stage_{stage}", lang)


def soil_label(soil: str, lang: str) -> str:
    return t(f"soil_{soil}", lang)


def moisture_label(m: str, lang: str) -> str:
    return t(f"moisture_{m}", lang)


def rating_label(rating: str, lang: str) -> str:
    return t(f"rating_{rating}", lang)


def activity_label(act: str, lang: str) -> str:
    return t(f"act_{act}", lang)


def severity_label(sev: str, lang: str) -> str:
    return t(f"sev_{sev}", lang)
