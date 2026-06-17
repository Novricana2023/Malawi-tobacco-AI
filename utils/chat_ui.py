"""Farmer chat UI — reusable on Home and chat page."""

from __future__ import annotations

import streamlit as st

from utils.farmer_chatbot import QUICK_PROMPTS
from utils.i18n import t
from utils.openai_chatbot import get_chatbot_response, is_openai_available


def get_welcome_message(lang: str) -> str:
    return t("chat_welcome", lang)


def ensure_welcome_message(lang: str) -> None:
    welcome = get_welcome_message(lang)
    if not st.session_state.chat_messages:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": welcome, "source": "welcome"}
        ]
    elif (
        len(st.session_state.chat_messages) == 1
        and st.session_state.chat_messages[0].get("source") == "welcome"
    ):
        st.session_state.chat_messages[0]["content"] = welcome


def send_chat_message(text: str, lang: str) -> None:
    history = [m for m in st.session_state.chat_messages if m["role"] in ("user", "assistant")]
    result = get_chatbot_response(text, history=history, language=lang)
    st.session_state.chat_messages.append({"role": "user", "content": text})
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": result["content"], "source": result["source"]}
    )


def render_farmer_chat(lang: str, compact: bool = False) -> None:
    ensure_welcome_message(lang)

    st.markdown(f"### {t('chat_title', lang)}")
    st.caption(t("chat_subtitle", lang))

    if is_openai_available():
        st.caption(t("chat_openai_on", lang))
    else:
        st.caption(t("chat_openai_off", lang))

    chat_height = 280 if compact else 320
    chat_box = st.container(height=chat_height)
    with chat_box:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    prompts = QUICK_PROMPTS.get(lang, QUICK_PROMPTS["en"])
    st.markdown(f"**{t('chat_quick', lang)}**")
    cols = st.columns(min(len(prompts), 4))
    for i, p in enumerate(prompts[:4]):
        if cols[i].button(p, key=f"home_quick_{lang}_{i}"):
            send_chat_message(p, lang)
            st.rerun()

    user_input = st.chat_input(t("chat_placeholder", lang), key=f"chat_input_{lang}")

    if user_input:
        send_chat_message(user_input, lang)
        st.rerun()

    if st.button(t("chat_clear", lang), key=f"clear_chat_{lang}"):
        st.session_state.chat_messages = []
        ensure_welcome_message(lang)
        st.rerun()

    st.caption(t("advisory_only", lang))
