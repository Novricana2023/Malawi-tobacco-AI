"""About — project information for farmers."""

import streamlit as st

from utils.i18n import t
from utils.ui_helpers import inject_custom_css, show_asset_image, show_logo

st.set_page_config(page_title="About", layout="wide")
inject_custom_css()

show_logo(120)
st.title(f"{t('about', 'en')} | {t('about', 'ny')}")

st.markdown(
    """
### Purpose / Cholinga
This tool helps **smallholder tobacco farmers in Malawi** make practical daily decisions:
- Check leaf diseases early / Onani matenda a masamba msanga
- Understand if soil is good for tobacco / Dziwani ngati dothi ndi labwino pa fodya
- Respond to weather risks / Samalitsani nyengo
- Estimate yield and track farm notes / Yezani kukolola ndi lembani za munda
- See market price trends / Onani mitengo ya msika

### Who is it for? / Akuti ndani?
Low-resource farmers — not large commercial estates. Designed for shared phones and slow connections.  
Alimi aang'ono — osati mafamu akulu. Zopangidwa kuti zigwire pa foni kapena pa neti yofoka.

### Farmer Chat / Kukambirana
Use **Farmer Chat** page to ask questions in **English or Chichewa** about disease, soil, weather, harvest, and prices.  
Gwiritsani ntchito **Farmer Chat** kufunsa m'Chingerezi kapena **Chichewa**.

### Important / Zofunika
- All disease results are **advisory only**, not medical certainty.
- Chotsani zizindikilo zokha — si chitsimikizo cha matenda.
- Weather and market data use sample values until connected to live services.

### Languages / Chilankhulo
English with Chichewa labels and chat support on key screens.

---
*Built for Malawian smallholder farmers — simplicity over complexity.*  
*Zopangidwa kwa alimi aang'ono a fodya ku Malawi.*
"""
)

show_asset_image("sample_harvest.png", caption="Supporting smallholder farmers across Malawi")
