# Malawi Tobacco AI — Farmer Assist

**Empowering smallholder tobacco farmers in Malawi with early disease detection, soil guidance, weather alerts, and bilingual farming support — right from a phone.**

## Impact

| Challenge | How this app helps |
|-----------|-------------------|
| **Crop loss from late disease detection** | Farmers check leaf symptoms or upload photos and get simple next-step advice before losses spread |
| **Poor soil & fertilizer decisions** | Soil type, moisture, and pH inputs return clear ratings and practical fertilizer tips |
| **Weather-related harvest losses** | Rain, heat, and drying warnings help farmers avoid curing tobacco on bad days |
| **Low digital literacy & language barriers** | Large buttons, simple layout, and **English + Chichewa** on key screens including home-page chat |
| **Limited extension worker access** | 24/7 advisory chat and field tools reach remote smallholders on shared phones |
| **Uncertain market timing** | Price trends and sell/hold guidance support better harvest and sales decisions |

**Built for real Malawian smallholders** — not commercial estates. Works offline with sample data; OpenAI optional for smarter chat.

## Features

- **Home Dashboard + Farmer Chat** — bilingual companion on the home page
- **My Tobacco Field** — field size, crop stage, yield estimate
- **Leaf Disease Checker** — photo upload or symptoms + sample leaf images
- **Soil Check** — soil type, pH, moisture → rating & fertilizer advice
- **Weather & Farming Advice** — practical daily field guidance
- **Market Price Guide** — price chart and sell/hold advice
- **Upload** — leaf images and farm records (optional)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501**

## Deploy on Streamlit Cloud

1. Repo: [github.com/Novricana2023/Malawi-tobacco-AI](https://github.com/Novricana2023/Malawi-tobacco-AI)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Main file: `app.py`
4. Add secret: `OPENAI_API_KEY` (optional, for smart chat)

## Notes

- Disease results are **advisory only** — not a medical diagnosis
- Farmer Chat works in **English and Chichewa**
- Designed for low-resource farmers on mobile devices
