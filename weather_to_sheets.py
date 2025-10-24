import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

CITY = input("Enter city name: ")

geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={CITY}&count=1"
geo_response = requests.get(geo_url)
geo_data = geo_response.json()

if "results" not in geo_data or not geo_data["results"]:
    print(f"❌ City '{CITY}' not found.")
    exit()

lat = geo_data["results"][0]["latitude"]
lon = geo_data["results"][0]["longitude"]

weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
weather_response = requests.get(weather_url)
weather_data = weather_response.json()
weather = weather_data["current_weather"]

temperature = weather["temperature"]
wind_speed = weather["windspeed"]
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("weather-creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("WeatherData").sheet1

sheet.append_row([time_now, CITY, temperature, wind_speed])
print(f"Logged: {CITY} | Temp: {temperature}°C | Wind Speed: {wind_speed} km/h at {time_now}")
