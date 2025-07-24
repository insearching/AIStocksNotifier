import os
from typing import List, Dict

import requests
import yfinance as yf
from twilio.rest import Client


def fetch_stock_data(tickers: List[str]) -> Dict[str, yf.Ticker]:
    """Fetch yfinance ticker objects for each symbol."""
    return {ticker: yf.Ticker(ticker) for ticker in tickers}


def get_latest_price(ticker: yf.Ticker) -> float:
    hist = ticker.history(period="1d")
    if hist.empty:
        return 0.0
    return hist["Close"].iloc[-1]


def moving_average(ticker: yf.Ticker, window: int = 20) -> float:
    hist = ticker.history(period=f"{window}d")
    if hist.empty:
        return 0.0
    return hist["Close"].mean()


def get_volume_ratio(ticker: yf.Ticker, window: int = 20) -> float:
    hist = ticker.history(period=f"{window}d")
    if hist.empty:
        return 0.0
    latest_volume = hist["Volume"].iloc[-1]
    avg_volume = hist["Volume"].mean()
    return latest_volume / avg_volume if avg_volume else 0.0


def fetch_news(query: str, api_key: str, page_size: int = 3) -> List[str]:
    url = (
        "https://newsapi.org/v2/everything?" f"q={query}&sortBy=publishedAt&pageSize={page_size}&apiKey={api_key}"
    )
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return []
    data = resp.json()
    return [a["title"] for a in data.get("articles", [])]


def should_notify(price: float, ma: float, volume_ratio: float) -> bool:
    if price > ma and volume_ratio > 1.5:
        return True
    return False


def send_sms(body: str) -> None:
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_phone = os.environ.get("TWILIO_FROM_PHONE")
    to_phone = os.environ.get("TWILIO_TO_PHONE")
    if not all([account_sid, auth_token, from_phone, to_phone]):
        print("Twilio credentials not fully provided.")
        return
    client = Client(account_sid, auth_token)
    client.messages.create(body=body, from_=from_phone, to=to_phone)


def main():
    tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]
    news_key = os.environ.get("NEWS_API_KEY")

    stocks = fetch_stock_data(tickers)
    messages = []
    for symbol, ticker in stocks.items():
        price = get_latest_price(ticker)
        ma20 = moving_average(ticker, 20)
        volume_ratio = get_volume_ratio(ticker, 20)
        if should_notify(price, ma20, volume_ratio):
            news_titles = fetch_news(symbol, news_key) if news_key else []
            news_text = "\n".join(news_titles)
            msg = (
                f"{symbol} alert! Price: {price:.2f} > MA20 {ma20:.2f}; "
                f"Volume ratio: {volume_ratio:.2f}.\n{news_text}"
            )
            messages.append(msg)
    if messages:
        send_sms("\n\n".join(messages))


if __name__ == "__main__":
    main()
