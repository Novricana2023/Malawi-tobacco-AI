"""OpenAI-powered farmer chat with offline fallback."""

from __future__ import annotations

import os
from typing import Any

from utils.farmer_chatbot import get_offline_response

SYSTEM_PROMPT = """You are a practical agricultural assistant and tobacco farming companion for smallholder farmers in Malawi.
Your name role: a friendly farming companion (bwenzi la alimi a fodya).
Use simple, clear language suitable for low-literacy farmers on mobile phones.

When greeting or introducing yourself:
- English: "Hello! I'm your tobacco farming companion. I can answer all your questions about tobacco farming."
- Chichewa: "Mulibwanji! Ndine bwenzi lanu la alimi a fodya. Nditha kuyankha mafunso anu onse okhudza fodya."

Help with:
- Tobacco leaf diseases (mosaic virus, black shank, blue mold, leaf spot, bacterial wilt)
- Soil suitability, pH, fertilizer, compost
- Weather, rain, heat, drying and curing tobacco
- Harvest timing, yield, field management
- Market prices and when to sell

Rules:
- Keep answers short: 3–6 sentences maximum
- Give practical steps the farmer can do today
- This is advisory only — not a medical or legal diagnosis
- If unsure, recommend visiting the local Agriculture Extension office
"""


def _get_api_key() -> str | None:
    """Load API key from Streamlit secrets or environment variable."""
    try:
        import streamlit as st

        if "OPENAI_API_KEY" in st.secrets:
            return str(st.secrets["OPENAI_API_KEY"])
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY")


def is_openai_available() -> bool:
    key = _get_api_key()
    return bool(key and key.strip() and not key.startswith("YOUR_"))


def get_openai_response(
    prompt: str,
    history: list[dict[str, str]] | None = None,
    language: str = "en",
) -> str:
    """Call OpenAI Chat Completions API. Raises on failure."""
    from openai import OpenAI

    api_key = _get_api_key()
    if not api_key:
        raise ValueError("OpenAI API key not configured")

    lang_note = (
        "Respond in Chichewa (Chinyanja). Use simple Chichewa words farmers understand."
        if language == "ny"
        else "Respond in English."
    )

    client = OpenAI(api_key=api_key)
    messages: list[dict[str, str]] = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{lang_note}"},
    ]

    for msg in (history or [])[-12:]:
        if msg.get("role") in ("user", "assistant") and msg.get("content"):
            messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": prompt.strip()})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=450,
        temperature=0.6,
    )
    return response.choices[0].message.content.strip()


def get_chatbot_response(
    prompt: str,
    history: list[dict[str, str]] | None = None,
    language: str = "en",
) -> dict[str, Any]:
    """
    Get chat reply — OpenAI if configured, otherwise offline rules.
    Returns dict with 'content' and 'source' ('openai' or 'offline').
    """
    if not prompt or not prompt.strip():
        from utils.i18n import t

        return {
            "content": t("chat_welcome", language),
            "source": "offline",
        }

    if is_openai_available():
        try:
            reply = get_openai_response(prompt, history, language)
            return {"content": reply, "source": "openai"}
        except Exception as exc:
            offline = get_offline_response(prompt, language)
            return {
                "content": f"{offline}\n\n_(OpenAI unavailable: {exc}. Showing offline answer.)_",
                "source": "offline",
            }

    return {"content": get_offline_response(prompt, language), "source": "offline"}
