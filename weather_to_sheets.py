import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

CITY = "Tbilisi"
LAT, LON = 41.7151, 44.8271
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("weather-creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("WeatherData").sheet1

response = requests.get(URL)
data = response.json()
weather = data.get("current_weather")

temperature = weather["temperature"]
wind_speed = weather["windspeed"]
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

sheet.append_row([time_now, CITY, temperature, wind_speed])
print(f"Logged: {CITY} | Temp: {temperature}°C | Wind Speed: {wind_speed} km/h at {time_now}")
