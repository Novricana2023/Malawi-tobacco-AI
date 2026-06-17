# Tobacco Farmer Assist Malawi

A simple, deployment-ready Streamlit app for **smallholder tobacco farmers in Malawi**.

## Features

- **Home Dashboard** — farm status, risk alerts, sample farm photos
- **My Tobacco Field** — field size, crop stage, yield estimate
- **Leaf Disease Checker** — photo upload or symptoms + sample leaf images
- **Soil Check** — soil type, pH, moisture → rating & fertilizer advice
- **Weather & Farming Advice** — offline sample weather with practical tips
- **Market Price Guide** — price chart and sell/hold advice
- **Farmer Chat** — ask questions in **English or Chichewa** (offline, no API key)
- **Upload** — leaf images and farm records (optional)
- **About** — farmer-focused information (no developer setup steps)

## Run locally

```bash
cd "Tobacco_Leaf_Disease_Assistant (3)"
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501**

## Deploy on Streamlit Cloud

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Main file: `app.py`

## Assets

Sample images and logo are in `assets/` for visual guidance on the home, disease, and market pages.

## Notes

- Disease detection is **advisory only** (rule-based + simple image heuristics)
- Farmer Chat works **offline** in English and Chichewa — no OpenAI required
- English + Chichewa labels throughout
