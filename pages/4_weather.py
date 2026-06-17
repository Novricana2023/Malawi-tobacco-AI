"""Weather & Farming Advice — mock/API-ready weather guidance."""

import streamlit as st

from utils.i18n import t
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot
from utils.weather_advisor import analyze_weather, get_mock_weather

st.set_page_config(page_title="Weather", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title(t("page_weather", lang))
st.caption(t("weather_caption", lang))

use_custom = st.checkbox(t("weather_manual", lang), value=False)

if use_custom:
    c1, c2 = st.columns(2)
    with c1:
        temp = st.number_input(f"{t('temperature', lang)} (°C)", 15.0, 45.0, 28.0)
        humidity = st.number_input(f"{t('humidity', lang)} (%)", 20.0, 100.0, 65.0)
    with c2:
        rain = st.number_input(f"{t('rain_today', lang)} (mm)", 0.0, 100.0, 3.0)
        rain_fc = st.number_input(f"{t('rain_forecast', lang)} (mm)", 0.0, 100.0, 12.0)
    weather = {"temp_c": temp, "humidity_pct": humidity, "rain_mm": rain, "rain_forecast_mm": rain_fc, "location": t("location", lang)}
else:
    weather = get_mock_weather(lang=lang)
    if st.button(t("btn_refresh_weather", lang)):
        import random
        from datetime import date

        weather = get_mock_weather(seed=date.today().toordinal() + random.randint(1, 999), lang=lang)

st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric(t("temperature", lang), f"{weather['temp_c']}°C")
m2.metric(t("humidity", lang), f"{weather.get('humidity_pct', 65)}%")
m3.metric(t("rain_today", lang), f"{weather.get('rain_mm', 0)} mm")
m4.metric(t("rain_forecast", lang), f"{weather.get('rain_forecast_mm', 0)} mm")

if st.button(t("btn_get_advice", lang), type="primary", use_container_width=True):
    result = analyze_weather(
        weather["temp_c"],
        weather.get("humidity_pct", 65),
        weather.get("rain_mm", 0),
        weather.get("rain_forecast_mm", 0),
        lang=lang,
    )
    st.session_state.weather_risk = result["overall_risk"]
    st.session_state._weather_result = result

result = st.session_state.get("_weather_result")

if not result:
    result = analyze_weather(
        weather["temp_c"],
        weather.get("humidity_pct", 65),
        weather.get("rain_mm", 0),
        weather.get("rain_forecast_mm", 0),
        lang=lang,
    )

st.divider()
st.markdown(f"### {t('alerts', lang)}")
for alert in result["alerts"]:
    label = (
        t("alert_rain", lang) if alert["type"] == "rain"
        else t("alert_heat", lang) if alert["type"] == "heat"
        else t("alert_disease", lang)
    )
    st.markdown(f"{risk_dot(alert['level'])} **{label}:** {alert['msg']}", unsafe_allow_html=True)

st.markdown(f"### {t('farmer_advice', lang)}")
for line in result["advice"]:
    st.write(f"• {line}")

if result.get("good_harvest_day"):
    st.success(t("good_harvest", lang))
