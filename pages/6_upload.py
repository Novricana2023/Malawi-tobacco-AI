"""Upload / Data Input — leaf images and simple farm records."""

import json
from datetime import datetime

import pandas as pd
import streamlit as st

from utils.disease_rules import analyze_image_simple
from utils.i18n import ACTIVITY_KEYS, activity_label, t
from utils.ui_helpers import init_session_state, inject_custom_css, show_asset_image

st.set_page_config(page_title="Upload", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title(t("page_upload", lang))
st.caption(t("upload_caption", lang))

tab1, tab2 = st.tabs([t("tab_leaf_images", lang), t("tab_farm_records", lang)])

with tab1:
    show_asset_image("sample_diseased_leaf.png", caption=t("upload_example", lang), width=280)

    files = st.file_uploader(
        t("upload_photos", lang),
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
    )
    if files and st.button(t("btn_analyze_all", lang), type="primary"):
        for f in files:
            result = analyze_image_simple(f.getvalue(), lang=lang)
            st.image(f, caption=f.name, width=200)
            st.write(f"**{result['disease']}** — {result['severity']} — {result['advice']}")
            st.session_state.last_disease_result = result

with tab2:
    st.markdown(t("record_intro", lang))
    record_date = st.date_input(t("date", lang), datetime.now())
    activity = st.selectbox(
        t("activity", lang),
        ACTIVITY_KEYS,
        format_func=lambda a: activity_label(a, lang),
    )
    notes = st.text_input(t("notes", lang), placeholder=t("notes_ph", lang))
    if st.button(t("btn_add_record", lang)):
        entry = {
            "date": str(record_date),
            "activity": activity_label(activity, lang),
            "notes": notes,
        }
        st.session_state.uploaded_records.append(entry)
        st.success(t("record_added", lang))

if st.session_state.uploaded_records:
    st.divider()
    st.markdown(f"### {t('your_records', lang)}")
    st.dataframe(pd.DataFrame(st.session_state.uploaded_records), use_container_width=True, hide_index=True)

    export = json.dumps(st.session_state.uploaded_records, indent=2, ensure_ascii=False)
    st.download_button(t("download_records", lang), export, file_name="farm_records.json", mime="application/json")
else:
    st.info(t("no_records", lang))
