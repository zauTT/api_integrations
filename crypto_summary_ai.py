from google import genai
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import os
os.chdir("/Users/zautt/Desktop/Python Projects/api_pratcie/api-integrations")

from dotenv import load_dotenv
load_dotenv(dotenv_path="/Users/zautt/Desktop/Python Projects/api_pratcie/api-integrations/.env")

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

crypto_data_sheet = client.open_by_key("1CXHaet9QS5Y2vgLDcnwamhZmjimmb2L8h03rEVv-v1c").sheet1
insight_spreadsheet = client.open_by_key("16EDG5qbgpUUhLOkGtaxYmEtZoMTbb0MXf4NgsEbcIvY")
try:
    insight_sheet = insight_spreadsheet.worksheet("AI_Insights")
except gspread.exceptions.WorksheetNotFound:
    insight_sheet = insight_spreadsheet.add_worksheet(title="AI_Insights", rows="100", cols="5")

insight_sheet.update_title("AI_Insights")
insight_spreadsheet.batch_update({
    "requests": [
        {"updateSheetProperties": {
            "properties": {"sheetId": insight_sheet.id, "index": 0},
            "fields": "index"
        }}
    ]
})

records = crypto_data_sheet.get_all_records()
df = pd.DataFrame(records)

if df.empty:
    print("No data found in the spreadsheet.")
    exit()

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else df.iloc[-1]

btc = float(latest["BTC (USD)"])
eth = float(latest["ETH (USD)"])
btc_change = latest["BTC (USD)"] - prev["BTC (USD)"]
eth_change = latest["ETH (USD)"] - prev["ETH (USD)"]

prompt = f"""
Recent crypto data:

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

summery = response.text.strip()

print("🧠 Gemini Summary:")
print(response.text)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"➡️ Writing to sheet: {insight_sheet.title} in {insight_spreadsheet.title}")
insight_sheet.append_row([timestamp, float(btc), float(eth), summery])
print(f"✅ Logged summary to AI_Insights at {timestamp}.")

print("🧩 Writing to spreadsheet URL:")
print(insight_spreadsheet.url)

print("🧩 Worksheet URL:")
print(insight_sheet.url)