"""Upload / Data Input — leaf images and simple farm records."""

import json
from datetime import datetime

import pandas as pd
import streamlit as st

from utils.disease_rules import analyze_image_simple
from utils.ui_helpers import init_session_state, inject_custom_css, show_asset_image

st.set_page_config(page_title="Upload", layout="wide")
inject_custom_css()
init_session_state()

st.title("Upload / Data Input")
st.caption("Works without uploads — use fallback mode below")

tab1, tab2 = st.tabs(["Leaf Images", "Farm Records"])

with tab1:
    show_asset_image("sample_diseased_leaf.png", caption="Example: upload a photo like this for checking", width=280)

    files = st.file_uploader(
        "Upload leaf photos",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
    )
    if files and st.button("Analyze all uploads", type="primary"):
        for f in files:
            result = analyze_image_simple(f.getvalue())
            st.image(f, caption=f.name, width=200)
            st.write(f"**{result['disease']}** — {result['severity']} — {result['advice']}")
            st.session_state.last_disease_result = result

with tab2:
    st.markdown("Simple farm record (saved in this session only)")
    record_date = st.date_input("Date", datetime.now())
    activity = st.selectbox(
        "Activity",
        ["Planting", "Transplanting", "Spraying", "Harvesting", "Drying", "Other"],
    )
    notes = st.text_input("Notes", placeholder="e.g. Applied fungicide on east field")
    if st.button("Add record"):
        entry = {
            "date": str(record_date),
            "activity": activity,
            "notes": notes,
        }
        st.session_state.uploaded_records.append(entry)
        st.success("Record added!")

if st.session_state.uploaded_records:
    st.divider()
    st.markdown("### Your Records")
    st.dataframe(pd.DataFrame(st.session_state.uploaded_records), use_container_width=True, hide_index=True)

    export = json.dumps(st.session_state.uploaded_records, indent=2)
    st.download_button("Download records (JSON)", export, file_name="farm_records.json", mime="application/json")
else:
    st.info("No records yet — add one above or use other pages without uploading anything.")
