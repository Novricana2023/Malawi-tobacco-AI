"""Market Price Guide — tobacco prices and selling advice."""

import plotly.express as px
import streamlit as st

from utils.market_data import get_market_advice, load_prices
from utils.ui_helpers import init_session_state, inject_custom_css, risk_dot, show_asset_image

st.set_page_config(page_title="Market Prices", layout="wide")
inject_custom_css()
init_session_state()

st.title("Market Price Guide")
st.caption("Burley tobacco — sample prices for Lilongwe auction floors (MWK per kg)")

show_asset_image("sample_harvest.png", caption="Harvest timing and market prices go together")

market = get_market_advice()
df = market["dataframe"]

c1, c2, c3 = st.columns(3)
c1.metric("Current price", f"MWK {market['current_price_mwk']:,.0f}/kg")
c2.metric("4-week average", f"MWK {market['avg_4_week_mwk']:,.0f}/kg")
c3.metric("Weekly change", f"{market['weekly_change']:+.0f} MWK")

st.markdown(f"### {market['action']} {risk_dot(market['signal'])}", unsafe_allow_html=True)
st.caption(market["action_ny"])

fig = px.line(
    df,
    x="Date",
    y="Price_MWK_per_kg",
    markers=True,
    title="Tobacco Price Trend",
    labels={"Price_MWK_per_kg": "Price (MWK/kg)", "Date": "Date"},
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
