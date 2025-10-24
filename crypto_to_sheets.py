import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
response = requests.get(url)
data = response.json()

btc_price = data["bitcoin"]["usd"]
eth_price = data["ethereum"]["usd"]
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("weather-creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("CryptoData").sheet1

sheet.append_row([time_now, btc_price, eth_price])
print(f"✅ Logged: BTC ${btc_price} | ETH ${eth_price} at {time_now}")
