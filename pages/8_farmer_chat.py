"""Farmer Chat — same chat as home page (full view)."""

import streamlit as st

from utils.chat_ui import render_farmer_chat
from utils.ui_helpers import init_session_state, inject_custom_css, show_logo

st.set_page_config(page_title="Farmer Chat", page_icon="🍃", layout="wide")
inject_custom_css()
init_session_state()

show_logo(90)
render_farmer_chat(st.session_state.lang, compact=False)
