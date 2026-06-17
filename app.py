"""
Tobacco Farmer Assist Malawi — main entry point.
Run: streamlit run app.py
"""

import streamlit as st

from utils.chat_ui import render_farmer_chat
from utils.i18n import t
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
    page_title="Tobacco Farmer Assist Malawi",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
init_session_state()

with st.sidebar:
    show_logo(width=110)
    st.markdown("### Farmer Assist Malawi")
    lang_choice = st.radio("Language / Chilankhulo", ["English", "Chichewa"], index=0)
    prev_lang = st.session_state.get("lang", "en")
    st.session_state.lang = "ny" if lang_choice == "Chichewa" else "en"
    if prev_lang != st.session_state.lang:
        st.session_state.chat_messages = []
    st.divider()
    st.caption("Made for smallholder tobacco farmers in Malawi.")

lang = st.session_state.lang

show_hero_banner()

st.markdown(f'<p class="main-header">{t("app_title", lang)}</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="sub-header">{t("welcome", lang)} &nbsp;|&nbsp; {t("welcome", "ny" if lang == "en" else "en")}</p>',
    unsafe_allow_html=True,
)

st.divider()

# Farmer Chat — main feature on home page
render_farmer_chat(lang)

st.divider()

weather = get_mock_weather()
weather_result = analyze_weather(
    weather["temp_c"],
    weather["humidity_pct"],
    weather["rain_mm"],
    weather["rain_forecast_mm"],
)
st.session_state.weather_risk = weather_result["overall_risk"]

market = get_market_advice()
yield_info = estimate_yield(
    st.session_state.field_hectares,
    st.session_state.crop_stage,
    st.session_state.soil_rating,
    st.session_state.disease_risk,
)

st.subheader(t("farm_status", lang))

col1, col2, col3 = st.columns(3)
with col1:
    risk_badge(st.session_state.disease_risk, t("disease_risk", lang), t("disease_risk", "ny"))
with col2:
    risk_badge(st.session_state.weather_risk, t("weather_risk", lang), t("weather_risk", "ny"))
with col3:
    soil_color = {"Good": "green", "Medium": "yellow", "Poor": "red"}.get(
        st.session_state.soil_rating, "yellow"
    )
    risk_badge(soil_color, t("soil_risk", lang), t("soil_risk", "ny"))

st.divider()

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card(
        t("estimated_yield", lang),
        f"{yield_info['harvest_potential_kg']:.0f} kg",
        f"~{yield_info['bags_estimate']} bags",
    )
with m2:
    metric_card("Field size", f"{st.session_state.field_hectares} ha", st.session_state.crop_stage)
with m3:
    metric_card("Temperature", f"{weather['temp_c']}°C", weather["location"])
with m4:
    metric_card(
        t("market_prices", lang),
        f"MWK {market['current_price_mwk']:,.0f}/kg",
        market["action"][:40] + "…",
    )

st.divider()

img1, img2 = st.columns(2)
with img1:
    show_asset_image("sample_harvest.png", caption="Harvest season — smallholder tobacco")
with img2:
    show_asset_image("sample_healthy_leaf.png", caption=t("sample_healthy", lang))

st.divider()

st.markdown("### Quick Actions")
qa1, qa2, qa3 = st.columns(3)
with qa1:
    if st.button("Check Leaf Disease", use_container_width=True):
        st.switch_page("pages/2_disease_checker.py")
with qa2:
    if st.button("Check Soil", use_container_width=True):
        st.switch_page("pages/3_soil_check.py")
with qa3:
    if st.button("Weather Advice", use_container_width=True):
        st.switch_page("pages/4_weather.py")

if weather_result["good_harvest_day"]:
    st.success(f"{t('good_harvest', lang)} | {t('good_harvest', 'ny')}")
else:
    st.warning("Check weather page before field work or drying tobacco.")

st.info(t("advisory_only", lang))

if st.session_state.last_disease_result:
    st.divider()
    st.markdown("### Latest Disease Check")
    r = st.session_state.last_disease_result
    st.write(f"**{r['disease']}** ({r.get('chichewa_name', '')}) — Severity: **{r['severity'].upper()}**")
    st.write(r["advice"])
