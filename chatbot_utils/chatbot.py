"""
Chatbot wrapper — OpenAI when configured, offline fallback otherwise.
"""

from utils.openai_chatbot import get_chatbot_response as _get_reply


def get_chatbot_response(prompt, history=None, language="en"):
    lang = "ny" if language in ("ny", "chichewa", "Chichewa") else "en"
    result = _get_reply(prompt, history=history, language=lang)
    return result["content"]
