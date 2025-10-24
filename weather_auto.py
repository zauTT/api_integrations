import schedule
import time
import subprocess

def run_weather():
    print("🌦 Running weather_to_sheets.py...")
    subprocess.run(["python3", "weather_to_sheets.py"])

schedule.every(30).minutes.do(run_weather)

print("✅ Weather auto-logger started (runs every 30 minutes)")
while True:
    schedule.run_pending()
    time.sleep(1)