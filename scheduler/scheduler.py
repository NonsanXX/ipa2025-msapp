import time
import os

from bson import json_util
from producer import produce
from database import get_router_info


def scheduler():
    INTERVAL = 30.0
    host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    count = 0

    # first tick happens immediately, next one is aligned
    next_run = time.monotonic()

    while True:
        now = time.time()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        ms = int((now % 1) * 1000)
        print(f"[{now_str}.{ms:03d}] run #{count}")

        start = time.monotonic()
        try:
            for data in get_router_info():
                body_bytes = json_util.dumps(data).encode("utf-8")
                produce(host, body_bytes)
        except Exception as e:
            print("Error:", e)

        # schedule next run exactly 30s after the previous scheduled one
        next_run += INTERVAL
        sleep_time = max(0.0, next_run - time.monotonic())
        print(f"  work took {time.monotonic() - start:.2f}s, sleeping {sleep_time:.2f}s")
        time.sleep(sleep_time)

        count += 1


if __name__ == "__main__":
    scheduler()
