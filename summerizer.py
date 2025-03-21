
import requests
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("")  # ✅ Corrected API Key loading

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
