"""About — project information for farmers."""

import streamlit as st

from utils.i18n import t
from utils.ui_helpers import inject_custom_css, show_asset_image, show_logo

st.set_page_config(page_title="About", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

show_logo(120)
st.title(t("about", lang))

st.markdown(f"### {t('about_purpose_h', lang)}")
st.markdown(t("about_purpose", lang))

st.markdown(f"### {t('about_who_h', lang)}")
st.markdown(t("about_who", lang))

st.markdown(f"### {t('about_chat_h', lang)}")
st.markdown(t("about_chat", lang))

st.markdown(f"### {t('about_important_h', lang)}")
st.markdown(t("about_important", lang))

st.markdown(f"*{t('about_footer', lang)}*")

show_asset_image("sample_harvest.png", caption=t("about_image_caption", lang))
