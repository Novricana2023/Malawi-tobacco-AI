"""Farmer chat UI — reusable on Home and chat page."""

from __future__ import annotations

import streamlit as st

from utils.farmer_chatbot import QUICK_PROMPTS
from utils.i18n import t
from utils.openai_chatbot import get_chatbot_response, is_openai_available


def get_welcome_message(lang: str) -> str:
    return t("chat_welcome", lang)


def ensure_welcome_message(lang: str) -> None:
    """Show bilingual welcome as first message when chat is empty."""
    if not st.session_state.chat_messages:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": get_welcome_message(lang), "source": "welcome"}
        ]


def send_chat_message(text: str, lang: str) -> None:
    history = [m for m in st.session_state.chat_messages if m["role"] in ("user", "assistant")]
    result = get_chatbot_response(text, history=history, language=lang)
    st.session_state.chat_messages.append({"role": "user", "content": text})
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": result["content"], "source": result["source"]}
    )


def render_farmer_chat(lang: str, compact: bool = False) -> None:
    """Render the farmer chat box."""
    ensure_welcome_message(lang)

    st.markdown(f"### {t('chat_title', lang)}")
    st.caption(f"{t('chat_subtitle', lang)} | {t('chat_subtitle', 'ny' if lang == 'en' else 'en')}")

    if is_openai_available():
        st.caption("Smart answers powered by OpenAI")
    else:
        st.caption("Offline mode — add OpenAI key for smarter answers")

    chat_height = 280 if compact else 320
    chat_box = st.container(height=chat_height)
    with chat_box:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    prompts = QUICK_PROMPTS.get(lang, QUICK_PROMPTS["en"])
    st.markdown("**Quick questions / Mafunso:**")
    cols = st.columns(min(len(prompts), 4))
    for i, p in enumerate(prompts[:4]):
        if cols[i].button(p, key=f"home_quick_{lang}_{i}"):
            send_chat_message(p, lang)
            st.rerun()

    user_input = st.chat_input(t("chat_placeholder", lang), key=f"chat_input_{lang}")

    if user_input:
        send_chat_message(user_input, lang)
        st.rerun()

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Clear chat", key=f"clear_chat_{lang}"):
            st.session_state.chat_messages = []
            ensure_welcome_message(lang)
            st.rerun()

    st.caption(t("advisory_only", lang))
