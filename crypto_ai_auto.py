import schedule
import time
import subprocess

def run_summery():
    print("🔄 Running crypto_summary_ai.py...")
    subprocess.run(["python3", "crypto_summary_ai.py"])

schedule.every(6).hours.do(run_summery)

print("✅ Crypto AI auto-summery started (runs every 6 hours)")
run_summery()

while True:
    schedule.run_pending()
    time.sleep(60)