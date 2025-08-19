import pika
import os

def produce(host, body):
    username = os.environ.get("RABBITMQ_DEFAULT_USER")
    password = os.environ.get("RABBITMQ_DEFAULT_PASS")
    credentials = pika.PlainCredentials(username, password)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))

    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key="check_interfaces")

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)
    connection.close()

if __name__ == "__main__":
    host = os.environ.get("RABBITMQ_HOST", "rabbitmq")  # ใช้ชื่อ service
    produce(host, b"192.168.1.44")