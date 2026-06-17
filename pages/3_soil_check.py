"""Soil Check — suitability and fertilizer advice for tobacco."""

import streamlit as st

from utils.i18n import t
from utils.soil_advisor import MOISTURE_LEVELS, SOIL_TYPES, evaluate_soil
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot, show_asset_image

st.set_page_config(page_title="Soil Check", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title("Soil Check")
st.caption("Important for Malawi smallholder fields — loamy soils in Kasungu, Lilongwe & Mzimba")

show_asset_image("hero_farm.png", caption="Tobacco field — soil health matters")

col1, col2 = st.columns([1, 1])

with col1:
    soil_type = st.selectbox(t("soil_type", lang), SOIL_TYPES)
    know_ph = st.checkbox("I know my soil pH", value=False)
    ph = None
    if know_ph:
        ph = st.slider("pH level", 4.0, 8.5, 6.0, 0.1)
    else:
        st.caption("pH unknown? Skip — visit your extension office for free testing.")

    moisture = st.selectbox(t("moisture", lang), MOISTURE_LEVELS)

with col2:
    if st.button("Check Soil", type="primary", use_container_width=True):
        result = evaluate_soil(soil_type, ph, moisture)
        st.session_state.soil_rating = result["rating"]
        st.session_state._soil_result = result

result = st.session_state.get("_soil_result")

if result:
    st.divider()
    st.markdown(
        f"### Rating: **{result['rating']}** ({result['rating_ny']}) {risk_dot(result['color'])}",
        unsafe_allow_html=True,
    )
    st.markdown("#### Fertilizer Advice")
    st.info(result["fertilizer_advice"])
    st.markdown("#### Soil Improvement Tips")
    for tip in result["improvement_tips"]:
        st.write(f"• {tip}")
else:
    st.info("Enter your soil details and click **Check Soil**.")
