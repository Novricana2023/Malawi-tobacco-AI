"""My Tobacco Field — farm inputs and yield estimate."""

import streamlit as st

from utils.i18n import STAGE_KEYS, stage_label, t
from utils.ui_helpers import init_session_state, inject_custom_css, show_asset_image
from utils.yield_estimator import estimate_yield

st.set_page_config(page_title="My Field", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title(t("page_field", lang))
st.caption(t("field_size", lang))

show_asset_image("hero_farm.png")

col1, col2 = st.columns([1, 1])

with col1:
    hectares = st.number_input(
        t("field_size", lang),
        min_value=0.01,
        max_value=50.0,
        value=float(st.session_state.field_hectares),
        step=0.1,
        format="%.2f",
    )
    stage = st.selectbox(
        t("crop_stage", lang),
        STAGE_KEYS,
        index=STAGE_KEYS.index(st.session_state.crop_stage)
        if st.session_state.crop_stage in STAGE_KEYS
        else 2,
        format_func=lambda s: stage_label(s, lang),
    )
    notes = st.text_area(
        t("farm_notes", lang),
        value=st.session_state.farm_notes,
        placeholder=t("notes_placeholder", lang),
        height=120,
    )

with col2:
    st.markdown(f"#### {t('yield_estimate', lang)}")
    if st.button(t("btn_calculate", lang), type="primary", use_container_width=True):
        st.session_state.field_hectares = hectares
        st.session_state.crop_stage = stage
        st.session_state.farm_notes = notes

    result = estimate_yield(
        hectares,
        stage,
        st.session_state.soil_rating,
        st.session_state.disease_risk,
        lang=lang,
    )

    st.metric(t("current_estimate", lang), f"{result['current_estimate_kg']} kg")
    st.metric(t("harvest_potential", lang), f"{result['harvest_potential_kg']} kg")
    st.metric(t("approx_bags", lang), f"{result['bags_estimate']}")
    st.info(result["message"])

if st.button(t("btn_save", lang), use_container_width=True):
    st.session_state.field_hectares = hectares
    st.session_state.crop_stage = stage
    st.session_state.farm_notes = notes
    st.success(t("saved_ok", lang))
