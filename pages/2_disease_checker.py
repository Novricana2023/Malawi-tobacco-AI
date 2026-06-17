"""Leaf Disease Checker — image upload or symptom selection."""

import streamlit as st

from utils.disease_rules import analyze_image_simple, classify_by_symptoms, get_all_symptom_options
from utils.i18n import severity_label, t
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot, show_asset_image

st.set_page_config(page_title="Disease Checker", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title(t("page_disease", lang))
st.caption(t("advisory_only", lang))

st.markdown(f"### {t('compare_leaves', lang)}")
ex1, ex2 = st.columns(2)
with ex1:
    show_asset_image("sample_healthy_leaf.png", caption=t("sample_healthy", lang))
with ex2:
    show_asset_image("sample_diseased_leaf.png", caption=t("sample_diseased", lang))

st.divider()

tab_img, tab_sym = st.tabs([t("tab_upload", lang), t("tab_symptoms", lang)])

result = None

with tab_img:
    uploaded = st.file_uploader(
        t("upload_image", lang),
        type=["jpg", "jpeg", "png", "webp"],
        help=t("upload_help", lang),
    )
    if uploaded:
        st.image(uploaded, caption=t("uploaded_leaf", lang), use_container_width=True)
        if st.button(t("btn_analyze", lang), type="primary", key="analyze_img"):
            result = analyze_image_simple(uploaded.getvalue(), lang=lang)
            st.session_state.last_disease_result = result
            st.session_state.disease_risk = {
                "low": "green",
                "medium": "yellow",
                "high": "red",
            }.get(result["severity"], "yellow")

with tab_sym:
    symptoms = st.multiselect(
        t("select_symptoms", lang),
        get_all_symptom_options(lang),
        help=t("symptoms_help", lang),
    )
    if st.button(t("btn_check_symptoms", lang), type="primary", key="analyze_sym"):
        result = classify_by_symptoms(symptoms, lang=lang)
        st.session_state.last_disease_result = result
        sev = result["severity"]
        st.session_state.disease_risk = {"low": "green", "medium": "yellow", "high": "red"}.get(sev, "yellow")

display = result or st.session_state.last_disease_result

if display:
    st.divider()
    st.markdown(f"### {t('results', lang)}")

    sev = display.get("severity", "low")
    risk_level = {"low": "green", "medium": "yellow", "high": "red"}.get(sev, "yellow")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(t("likely_issue", lang), display.get("disease", t("unknown", lang)))
    with c2:
        st.markdown(
            f"**{t('severity_label', lang)}**  \n{risk_dot(risk_level)} {severity_label(sev, lang)}",
            unsafe_allow_html=True,
        )
    with c3:
        conf = display.get("confidence", 0)
        st.metric(t("confidence", lang), f"{conf * 100:.0f}%" if conf else "—")

    st.markdown(f"#### {t('what_to_do', lang)}")
    st.success(display.get("advice", ""))

    if display.get("method") == "image_heuristic":
        st.caption(t("image_heuristic_note", lang))

else:
    st.info(t("analyze_prompt", lang))
