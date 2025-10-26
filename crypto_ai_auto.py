import schedule
import time
import subprocess

def run_pipeline():
    print("\n🔁 Starting full crypto + AI summary pipeline...")

    print("💰 Fetching latest crypto prices...")
    subprocess.run(["python3", "crypto_auto.py"])

    print("🧠 Generating AI summary...")
    subprocess.run(["python3", "crypto_summary_ai.py"])

    print("✅ Pipeline completed.\n")

run_pipeline()

schedule.every(6).hours.do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)