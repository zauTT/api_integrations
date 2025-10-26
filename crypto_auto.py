import schedule
import time
import subprocess

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="/Users/zautt/Desktop/Python Projects/api_pratcie/api-integrations/.env")

def run_crypto():
    print("🔄 Running crypto_to_sheets.py...")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(["python3", "crypto_to_sheets.py"], check=True)
            print("✅ Script ran successfully.\n")
            break
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print("Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print("❌ All attempts failed. Please check the script for issues. Will retry in the next scheduled run.\n")


schedule.every(30).minutes.do(run_crypto)

print("✅ Crypto auto-logger started (runs every 30 minutes)")
while True:
    schedule.run_pending()
    time.sleep(1)