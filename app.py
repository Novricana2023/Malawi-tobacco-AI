"""
Tobacco Farmer Assist Malawi — main entry point.
Run: streamlit run app.py
"""

import streamlit as st

from utils.chat_ui import render_farmer_chat
from utils.i18n import stage_label, t
from utils.market_data import get_market_advice
from utils.ui_helpers import (
    init_session_state,
    inject_custom_css,
    metric_card,
    risk_badge,
    show_asset_image,
    show_hero_banner,
    show_logo,
)
from utils.weather_advisor import analyze_weather, get_mock_weather
from utils.yield_estimator import estimate_yield

st.set_page_config(
    page_title="Mlimi Smart Assistant",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
init_session_state()

with st.sidebar:
    show_logo(width=110)
    st.markdown(f"### {t('sidebar_title', st.session_state.get('lang', 'en'))}")
    lang_labels = {"English": "en", "Chichewa": "ny"}
    lang_choice = st.radio(
        t("lang_label", st.session_state.get("lang", "en")),
        list(lang_labels.keys()),
        index=0 if st.session_state.get("lang", "en") == "en" else 1,
    )
    prev_lang = st.session_state.get("lang", "en")
    st.session_state.lang = lang_labels[lang_choice]
    if prev_lang != st.session_state.lang:
        st.session_state.chat_messages = []
    st.divider()
    st.caption(t("sidebar_caption", st.session_state.lang))

lang = st.session_state.lang

show_hero_banner(lang)

st.markdown(f'<p class="sub-header">{t("welcome", lang)}</p>', unsafe_allow_html=True)

st.divider()
render_farmer_chat(lang)
st.divider()

weather = get_mock_weather(lang=lang)
weather_result = analyze_weather(
    weather["temp_c"],
    weather["humidity_pct"],
    weather["rain_mm"],
    weather["rain_forecast_mm"],
    lang=lang,
)
st.session_state.weather_risk = weather_result["overall_risk"]

market = get_market_advice(lang=lang)
yield_info = estimate_yield(
    st.session_state.field_hectares,
    st.session_state.crop_stage,
    st.session_state.soil_rating,
    st.session_state.disease_risk,
    lang=lang,
)

st.subheader(t("farm_status", lang))

col1, col2, col3 = st.columns(3)
with col1:
    risk_badge(st.session_state.disease_risk, t("disease_risk", lang))
with col2:
    risk_badge(st.session_state.weather_risk, t("weather_risk", lang))
with col3:
    soil_color = {"Good": "green", "Medium": "yellow", "Poor": "red"}.get(
        st.session_state.soil_rating, "yellow"
    )
    risk_badge(soil_color, t("soil_risk", lang))

st.divider()

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card(
        t("estimated_yield", lang),
        f"{yield_info['harvest_potential_kg']:.0f} kg",
        f"~{yield_info['bags_estimate']} {t('bags', lang)}",
    )
with m2:
    metric_card(
        t("field_size_label", lang),
        f"{st.session_state.field_hectares} ha",
        stage_label(st.session_state.crop_stage, lang),
    )
with m3:
    metric_card(t("temperature", lang), f"{weather['temp_c']}°C", weather["location"])
with m4:
    metric_card(
        t("market_prices", lang),
        f"MWK {market['current_price_mwk']:,.0f}/kg",
        market["action"][:45],
    )

st.divider()

img1, img2 = st.columns(2)
with img1:
    show_asset_image("sample_harvest.png", caption=t("harvest_caption", lang))
with img2:
    show_asset_image("sample_healthy_leaf.png", caption=t("sample_healthy", lang))

st.divider()

st.markdown(f"### {t('quick_actions', lang)}")
qa1, qa2, qa3 = st.columns(3)
with qa1:
    if st.button(t("btn_disease", lang), use_container_width=True):
        st.switch_page("pages/2_disease_checker.py")
with qa2:
    if st.button(t("btn_soil", lang), use_container_width=True):
        st.switch_page("pages/3_soil_check.py")
with qa3:
    if st.button(t("btn_weather", lang), use_container_width=True):
        st.switch_page("pages/4_weather.py")

if weather_result["good_harvest_day"]:
    st.success(t("good_harvest", lang))
else:
    st.warning(t("weather_check_warning", lang))

st.info(t("advisory_only", lang))

if st.session_state.last_disease_result:
    st.divider()
    st.markdown(f"### {t('latest_disease', lang)}")
    r = st.session_state.last_disease_result
    from utils.i18n import severity_label

    st.write(
        f"**{r['disease']}** — {t('severity_label', lang)}: **{severity_label(r['severity'], lang)}**"
    )
    st.write(r["advice"])
