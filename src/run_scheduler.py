# src/run_scheduler.py
import os, time, subprocess
from datetime import datetime, timedelta, timezone

# Use IST by default; Dockerfile sets TZ=Asia/Kolkata so time.localtime is IST
RUN_TIME = os.getenv("RUN_TIME", "17:28")  # HH:MM 24h, local container time
CMD = os.getenv("RUN_CMD", "python src/main.py")

def parse_time(tstr):
    h, m = tstr.split(":")
    return int(h), int(m)

def next_run(now, hh, mm):
    run = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if run <= now:
        run += timedelta(days=1)
    return run

def main():
    hh, mm = parse_time(RUN_TIME)
    while True:
        now = datetime.now()
        target = next_run(now, hh, mm)
        wait_s = (target - now).total_seconds()
        print(f"[scheduler] Now: {now:%Y-%m-%d %H:%M:%S} | Next run at: {target:%Y-%m-%d %H:%M:%S} | sleeping {int(wait_s)}s", flush=True)
        time.sleep(max(1, int(wait_s)))
        print("[scheduler] Running job…", flush=True)
        try:
            # run the pipeline as a subprocess so the loop survives errors
            result = subprocess.run(CMD, shell=True)
            print(f"[scheduler] Job exited with code {result.returncode}", flush=True)
        except Exception as e:
            print(f"[scheduler] Job crashed: {e}", flush=True)
        # small buffer to avoid re-running in the same minute if container wakes late
        time.sleep(5)

if __name__ == "__main__":
    main()