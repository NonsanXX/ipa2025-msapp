import pika
import os
import sys
import time
from callback import callback


def connect():
    username = os.environ.get("RABBITMQ_DEFAULT_USER")
    password = os.environ.get("RABBITMQ_DEFAULT_PASS")
    host = host = os.getenv("RABBITMQ_HOST")
    credentials = pika.PlainCredentials(username, password)

    # A few robustness tweaks
    params = pika.ConnectionParameters(
        host=host,
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=60,
        connection_attempts=10,
        retry_delay=3,
    )

    for attempt in range(10):
        print(f"Connecting to RabbitMQ (try {attempt+1})...")
        try:
            return pika.BlockingConnection(params)
        except pika.exceptions.AMQPConnectionError as e:
            print("Failed:", e)
            time.sleep(3)
    raise RuntimeError("RabbitMQ unreachable")


def consume():
    conn = connect()
    channel = conn.channel()
    channel.queue_declare(queue="router_jobs")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="router_jobs", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


if __name__ == "__main__":
    try:
        consume()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
