# AIStocksNotifier

This project provides a simple Python-based stock alert agent. It analyses the five popular tickers `AAPL`, `MSFT`, `TSLA`, `AMZN`, and `GOOGL` using historical price data from Yahoo Finance. When a stock's price closes above its 20‑day moving average with a high volume ratio, a notification is sent via SMS using Twilio. Optionally, the agent fetches recent news headlines for context using the NewsAPI service.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- A Twilio account for sending SMS messages
- (Optional) A NewsAPI key for fetching headlines

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the following environment variables:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_FROM_PHONE`
   - `TWILIO_TO_PHONE`
   - `NEWS_API_KEY` (optional)
3. Run the notifier:
   ```bash
   python stocks_notifier.py
   ```

The script checks each ticker and sends a combined SMS if any alerts are triggered.
