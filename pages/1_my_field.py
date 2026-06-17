"""My Tobacco Field — farm inputs and yield estimate."""

import streamlit as st

from utils.i18n import t
from utils.ui_helpers import init_session_state, inject_custom_css, show_asset_image
from utils.yield_estimator import STAGES, estimate_yield

st.set_page_config(page_title="My Field", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title("My Tobacco Field")
st.caption(f"{t('field_size', lang)} | {t('field_size', 'ny')}")

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
        STAGES,
        index=STAGES.index(st.session_state.crop_stage)
        if st.session_state.crop_stage in STAGES
        else 2,
    )
    notes = st.text_area(
        t("farm_notes", lang),
        value=st.session_state.farm_notes,
        placeholder="e.g. Transplanted on 15 Nov, north corner has wet soil…",
        height=120,
    )

with col2:
    st.markdown("#### Yield Estimate")
    if st.button("Calculate Yield", type="primary", use_container_width=True):
        st.session_state.field_hectares = hectares
        st.session_state.crop_stage = stage
        st.session_state.farm_notes = notes

    result = estimate_yield(
        hectares,
        stage,
        st.session_state.soil_rating,
        st.session_state.disease_risk,
    )

    st.metric("Current season estimate", f"{result['current_estimate_kg']} kg")
    st.metric("Potential at harvest", f"{result['harvest_potential_kg']} kg")
    st.metric("Approx. bags (~50 kg)", f"{result['bags_estimate']}")
    st.info(result["message"])

if st.button("Save Field Info", use_container_width=True):
    st.session_state.field_hectares = hectares
    st.session_state.crop_stage = stage
    st.session_state.farm_notes = notes
    st.success("Field information saved!")
