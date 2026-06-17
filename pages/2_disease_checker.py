"""Leaf Disease Checker — image upload or symptom selection."""

import streamlit as st

from utils.disease_rules import analyze_image_simple, classify_by_symptoms, get_all_symptom_options
from utils.i18n import t
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot, show_asset_image

st.set_page_config(page_title="Disease Checker", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title("Leaf Disease Checker")
st.caption(f"{t('advisory_only', lang)} | {t('advisory_only', 'ny')}")

# Sample reference images
st.markdown("### Compare your leaf with these examples")
ex1, ex2 = st.columns(2)
with ex1:
    show_asset_image("sample_healthy_leaf.png", caption=t("sample_healthy", lang))
with ex2:
    show_asset_image("sample_diseased_leaf.png", caption=t("sample_diseased", lang))

st.divider()

tab_img, tab_sym = st.tabs(["Upload Photo", "Select Symptoms"])

result = None

with tab_img:
    uploaded = st.file_uploader(
        t("upload_image", lang),
        type=["jpg", "jpeg", "png", "webp"],
        help="Take a clear photo of the affected leaf in daylight.",
    )
    if uploaded:
        st.image(uploaded, caption="Uploaded leaf", use_container_width=True)
        if st.button("Analyze Photo", type="primary", key="analyze_img"):
            result = analyze_image_simple(uploaded.getvalue())
            st.session_state.last_disease_result = result
            st.session_state.disease_risk = {
                "low": "green",
                "medium": "yellow",
                "high": "red",
            }.get(result["severity"], "yellow")

with tab_sym:
    symptoms = st.multiselect(
        t("select_symptoms", lang),
        get_all_symptom_options(),
        help="Choose all signs you see on the plant.",
    )
    if st.button("Check Symptoms", type="primary", key="analyze_sym"):
        result = classify_by_symptoms(symptoms)
        st.session_state.last_disease_result = result
        sev = result["severity"]
        st.session_state.disease_risk = {"low": "green", "medium": "yellow", "high": "red"}.get(sev, "yellow")

display = result or st.session_state.last_disease_result

if display:
    st.divider()
    st.markdown("### Results")

    sev = display.get("severity", "low")
    risk_level = {"low": "green", "medium": "yellow", "high": "red"}.get(sev, "yellow")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Likely issue", display.get("disease", "Unknown"))
    with c2:
        st.markdown(f"**Severity**  \n{risk_dot(risk_level)} {sev.upper()}", unsafe_allow_html=True)
    with c3:
        conf = display.get("confidence", 0)
        st.metric("Confidence", f"{conf * 100:.0f}%" if conf else "N/A")

    if display.get("chichewa_name"):
        st.write(f"**Chichewa:** {display['chichewa_name']}")

    st.markdown(f"#### {t('what_to_do', lang)}")
    st.success(display.get("advice", ""))

    if display.get("method") == "image_heuristic":
        st.caption("Analysis used simple image colors — for best results, also check symptoms manually.")

else:
    st.info("Upload a photo or select symptoms, then click Analyze.")
