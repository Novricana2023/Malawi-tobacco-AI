"""Weather & Farming Advice — mock/API-ready weather guidance."""

import streamlit as st

from utils.i18n import t
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot
from utils.weather_advisor import analyze_weather, get_mock_weather

st.set_page_config(page_title="Weather", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title("Weather & Farming Advice")
st.caption("Offline sample data — ready to connect to a weather service later")

use_custom = st.checkbox("Enter weather manually (optional)", value=False)

if use_custom:
    c1, c2 = st.columns(2)
    with c1:
        temp = st.number_input("Temperature (°C)", 15.0, 45.0, 28.0)
        humidity = st.number_input("Humidity (%)", 20.0, 100.0, 65.0)
    with c2:
        rain = st.number_input("Rain today (mm)", 0.0, 100.0, 3.0)
        rain_fc = st.number_input("Rain forecast 24h (mm)", 0.0, 100.0, 12.0)
    weather = {"temp_c": temp, "humidity_pct": humidity, "rain_mm": rain, "rain_forecast_mm": rain_fc}
else:
    weather = get_mock_weather()
    if st.button("Refresh weather data"):
        import random
        from datetime import date

        weather = get_mock_weather(seed=date.today().toordinal() + random.randint(1, 999))

st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Temperature", f"{weather['temp_c']}°C")
m2.metric("Humidity", f"{weather.get('humidity_pct', 65)}%")
m3.metric("Rain today", f"{weather.get('rain_mm', 0)} mm")
m4.metric("Rain forecast", f"{weather.get('rain_forecast_mm', 0)} mm")

if st.button("Get Advice", type="primary", use_container_width=True):
    result = analyze_weather(
        weather["temp_c"],
        weather.get("humidity_pct", 65),
        weather.get("rain_mm", 0),
        weather.get("rain_forecast_mm", 0),
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
    )

st.divider()
st.markdown("### Alerts")
for alert in result["alerts"]:
    label = "Rain" if alert["type"] == "rain" else "Heat" if alert["type"] == "heat" else "Disease"
    st.markdown(f"{risk_dot(alert['level'])} **{label}:** {alert['msg']}", unsafe_allow_html=True)

st.markdown("### Farmer Advice")
for line in result["advice"]:
    st.write(f"• {line}")

if result.get("good_harvest_day"):
    st.success(f"{t('good_harvest', lang)} | {t('good_harvest', 'ny')}")
