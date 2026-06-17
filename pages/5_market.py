"""Market Price Guide — tobacco prices and selling advice."""

import plotly.express as px
import streamlit as st

from utils.i18n import t
from utils.market_data import get_market_advice, load_prices
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot, show_asset_image

st.set_page_config(page_title="Market Prices", layout="wide")
inject_custom_css()
init_session_state()

lang = st.session_state.lang

st.title(t("page_market", lang))
st.caption(t("market_caption", lang))

show_asset_image("sample_harvest.png", caption=t("market_image_caption", lang))

market = get_market_advice(lang=lang)
df = market["dataframe"]

c1, c2, c3 = st.columns(3)
c1.metric(t("current_price", lang), f"MWK {market['current_price_mwk']:,.0f}/kg")
c2.metric(t("avg_4_week", lang), f"MWK {market['avg_4_week_mwk']:,.0f}/kg")
c3.metric(t("weekly_change", lang), f"{market['weekly_change']:+.0f} MWK")

st.markdown(f"### {market['action']} {risk_dot(market['signal'])}", unsafe_allow_html=True)

fig = px.line(
    df,
    x="Date",
    y="Price_MWK_per_kg",
    markers=True,
    title=t("price_trend", lang),
    labels={"Price_MWK_per_kg": t("price_axis", lang), "Date": t("date_axis", lang)},
)
fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    plot_bgcolor="#f8f9fa",
    paper_bgcolor="#ffffff",
)
fig.update_traces(line_color="#1a5c2e", marker_color="#2ecc71")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df.tail(8).sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
