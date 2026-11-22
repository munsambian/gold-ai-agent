# Gold Market Monitor — mobile web prototype

A Streamlit research dashboard using publicly accessible Yahoo Finance GC=F futures data. No broker login or API key required. **This is not a deployed website**, and no trade orders are placed.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open the local address shown by Streamlit on your computer.

## Publish for phone access
1. Put `app.py` and `requirements.txt` in a GitHub repository.
2. Create a Streamlit Community Cloud app and point it to `app.py` (subject to Streamlit hosting availability and terms).
3. Open the generated HTTPS URL from your phone.

## Limitations
GC=F is gold futures, not XAUUSD spot. Yahoo Finance is unofficial for automated programmatic access and may rate-limit or change availability. Historical candles may be delayed. This version uses fixed EMA and breakout rules, not an AI model. Do not use signals for live trading without proper data validation and backtesting.
