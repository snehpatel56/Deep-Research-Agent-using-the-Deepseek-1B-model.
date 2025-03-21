from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import requests

app = FastAPI()

# ✅ Replace with your Deepseek API Key
DEEPSEEK_API_KEY = ""

def get_52_week_high_stocks():
    """Fetches 52-week high stock prices for Indian market."""
    symbols = ["RELIANCE.NS", "TCS.NS", "SWIGGY.NS"]  # Add more NSE stocks
    results = []    

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1y", interval="1d")

        if history.empty:
            print(f"⚠️ No data found for {symbol}")
            continue

        max_price = history["High"].max()
        results.append({"Stock": symbol, "52-Week High": round(max_price, 2)})

    return pd.DataFrame(results)

def summarize_with_deepseek(text):
    """Summarizes research findings using Deepseek 1B API."""
    url = "https://api.deepseek.com/v1/models/deepseek-1b/completions"  # Update if needed

    headers = {
        "Authorization": f"Bearer {"sk-15ded6816aea4f5d872ceeeb60a0fc67"}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-1b",
        "messages": [
            {"role": "system", "content": "Summarize this research data."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Failed to summarize data."

@app.get("/stocks")
def fetch_stock_data():
    """Fetches stock data and returns summarized insights."""
    df = get_52_week_high_stocks()
    if df.empty:
        return {"message": "No stock data found"}

    summary = summarize_with_deepseek(df.to_string())
    return {"stocks": df.to_dict(orient="records"), "summary": summary}



import requests
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("sk-15ded6816aea4f5d872ceeeb60a0fc67")  # ✅ Corrected API Key loading

# API URL
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/models/deepseek-1b/completions"  # Check if this works

def summarize_with_deepseek(text):
    """Summarizes stock insights using Deepseek 1B API."""
    if not DEEPSEEK_API_KEY:
        return "Error: API Key is missing."

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-1b",
        "messages": [
            {"role": "system", "content": "Summarize this research data."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No summary available.")
    else:
        return f"❌ Error: {response.status_code}, Response: {response.text}"

def answer_question(question, context):
    """Answers user queries based on research data."""
    if not DEEPSEEK_API_KEY:
        return "Error: API Key is missing."

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-1b",
        "messages": [
            {"role": "system", "content": "You are a financial analyst. Answer based on the given data."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
        ]
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No answer available.")
    else:
        return f"❌ Error: {response.status_code}, Response: {response.text}"

if __name__ == "__main__":
    sample_text = "Reliance Industries hit a 52-week high due to strong earnings and new investment deals."
    
    # Test summarization
    print("🔹 Summary Output:")
    print(summarize_with_deepseek(sample_text))

    # Test Q&A
    question = "Why did Reliance stock rise?"
    print("\n🔹 Q&A Output:")
    print(answer_question(question, sample_text))
