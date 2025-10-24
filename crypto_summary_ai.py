import os
from dotenv import load_dotenv
load_dotenv()

from google import genai
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("weather-creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("CryptoData").sheet1

records = sheet.get_all_records()
df = pd.DataFrame(records)

if df.empty:
    print("No data found in the spreadsheet.")
    exit()

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else df.iloc[-1]

btc_change = latest["BTC (USD)"] - prev["BTC (USD)"]
eth_change = latest["ETH (USD)"] - prev["ETH (USD)"]

prompt = f"""
Here is the recent crypto data:

{df.tail(5).to_string(index=False)}

Bitcoin change: {btc_change: .2f} USD
Ethereum change: {eth_change: .2f} USD

Write a short 2-sentence summery of describing today's crypto trend.
"""

client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client_ai.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt]
)

print("🧠 Gemini Summary:")
print(response.text)


