import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_52_week_high_stocks():
    """Fetches NSE stocks that reached their 52-week high in the last month."""
    symbols = ["RELIANCE.NS", "TCS.NS", "SWIGGY.NS"]  
    results = []

    one_year_ago = datetime.today() - timedelta(days=365)
    one_month_ago = datetime.today() - timedelta(days=30)

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1y", interval="1d")

        if history.empty:
            print(f"⚠️ No data found for {symbol}")
            continue

        max_price = history["High"].max()  # 52-week high
        last_month_high = history.loc[history.index >= one_month_ago, "High"].max()  # High in last month

        if last_month_high == max_price:  # If last month high equals 52-week high
            results.append({"Stock": symbol, "52-Week High": round(max_price, 2)})

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = get_52_week_high_stocks()
    print(df)
