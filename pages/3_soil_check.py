"""Soil Check — suitability and fertilizer advice for tobacco."""

import streamlit as st

from utils.i18n import MOISTURE_KEYS, SOIL_KEYS, moisture_label, soil_label, t
from utils.soil_advisor import evaluate_soil
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot, show_asset_image

st.set_page_config(page_title="Soil Check", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title(t("page_soil", lang))
st.caption(t("soil_caption", lang))

show_asset_image("hero_farm.png", caption=t("soil_image_caption", lang))

col1, col2 = st.columns([1, 1])

with col1:
    soil_type = st.selectbox(
        t("soil_type", lang),
        SOIL_KEYS,
        format_func=lambda s: soil_label(s, lang),
    )
    know_ph = st.checkbox(t("know_ph", lang), value=False)
    ph = None
    if know_ph:
        ph = st.slider(t("ph_level", lang), 4.0, 8.5, 6.0, 0.1)
    else:
        st.caption(t("ph_unknown_tip", lang))

    moisture = st.selectbox(
        t("moisture", lang),
        MOISTURE_KEYS,
        format_func=lambda m: moisture_label(m, lang),
    )

with col2:
    if st.button(t("btn_check_soil", lang), type="primary", use_container_width=True):
        result = evaluate_soil(soil_type, ph, moisture, lang=lang)
        st.session_state.soil_rating = result["rating_key"]
        st.session_state._soil_result = result

result = st.session_state.get("_soil_result")

if result:
    st.divider()
    st.markdown(
        f"### {t('soil_rating', lang)}: **{result['rating']}** {risk_dot(result['color'])}",
        unsafe_allow_html=True,
    )
    st.markdown(f"#### {t('fertilizer_advice', lang)}")
    st.info(result["fertilizer_advice"])
    st.markdown(f"#### {t('soil_tips', lang)}")
    for tip in result["improvement_tips"]:
        st.write(f"• {tip}")
else:
    st.info(t("soil_enter_prompt", lang))
