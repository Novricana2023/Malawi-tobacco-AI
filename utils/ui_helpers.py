"""Shared UI components and styling for the Streamlit app."""

from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
THUMBS_DIR = ASSETS_DIR / "thumbs"

RISK_COLORS = {
    "green": "#2ecc71",
    "yellow": "#f1c40f",
    "red": "#e74c3c",
}


def asset_path(filename: str) -> Path:
    """Return best available image path (compressed thumb preferred)."""
    thumb = THUMBS_DIR / filename.replace(".png", ".jpg")
    if thumb.exists():
        return thumb
    thumb_png = THUMBS_DIR / filename
    if thumb_png.exists():
        return thumb_png
    original = ASSETS_DIR / filename
    return original


def show_logo(width: int = 100) -> None:
    logo = asset_path("logo.png")
    if logo.exists():
        st.image(str(logo), width=width)


def show_asset_image(filename: str, caption: str = "", width: int | None = None) -> None:
    """Display an asset using compressed version when available."""
    path = asset_path(filename)
    if not path.exists():
        return
    if width:
        st.image(str(path), caption=caption, width=width)
    else:
        st.image(str(path), caption=caption, use_container_width=True)


def risk_dot(level: str) -> str:
    color = RISK_COLORS.get(level, "#999")
    return f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color};margin-right:8px;"></span>'


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1a5c2e;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1rem;
            color: #555;
            margin-bottom: 1.5rem;
        }
        .risk-card {
            padding: 1rem 1.2rem;
            border-radius: 12px;
            border-left: 6px solid;
            background: #f8f9fa;
            margin-bottom: 0.8rem;
        }
        .risk-green { border-color: #2ecc71; }
        .risk-yellow { border-color: #f1c40f; }
        .risk-red { border-color: #e74c3c; }
        div[data-testid="stSidebar"] {
            background-color: #f0f7f2;
        }
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.6rem 1rem;
        }
        .hero-caption {
            font-size: 0.9rem;
            color: #666;
            margin-top: -0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(level: str, label_en: str, label_ny: str = "") -> None:
    dot = risk_dot(level)
    ny_text = f"<br><small>{label_ny}</small>" if label_ny else ""
    st.markdown(
        f"""
        <div class="risk-card risk-{level}">
            {dot}<strong>{label_en}</strong>{ny_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, subtitle: str = "") -> None:
    sub = f"<div style='font-size:0.85rem;color:#666;'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div style="background:#fff;border:1px solid #ddd;border-radius:10px;
                    padding:1rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
            <div style="font-size:0.9rem;color:#555;">{title}</div>
            <div style="font-size:1.6rem;font-weight:700;color:#1a5c2e;">{value}</div>
            {sub}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_hero_banner() -> None:
    path = asset_path("hero_farm.png")
    if path.exists():
        show_asset_image("hero_farm.png")
        st.markdown(
            '<p class="hero-caption">Smallholder tobacco fields — Central Region, Malawi</p>',
            unsafe_allow_html=True,
        )


def init_session_state() -> None:
    defaults = {
        "lang": "en",
        "field_hectares": 0.5,
        "crop_stage": "Growing",
        "farm_notes": "",
        "soil_rating": "Medium",
        "disease_risk": "green",
        "weather_risk": "green",
        "last_disease_result": None,
        "uploaded_records": [],
        "chat_messages": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
