import pika, os, sys, time, json
from get_interfaces import get_interfaces
from database import set_router_interfaces

def callback(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    ip = data['ip']
    usr = data['username']
    pwd = data['password']

    print(f"Received job for router {ip}")
    output = get_interfaces(ip, usr, pwd)
    print(json.dumps(output, indent=2))
    
    set_router_interfaces(ip, output)
    print(f"Stored interface status for {ip}")


def connect():
    username = os.environ.get("RABBITMQ_DEFAULT_USER")
    password = os.environ.get("RABBITMQ_DEFAULT_PASS")
    host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
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

    for i in range(10):
        print(f"Connecting to RabbitMQ (try {i+1})...")
        try:
            return pika.BlockingConnection(params)
        except pika.exceptions.AMQPConnectionError as e:
            print("Failed:", e)
            time.sleep(3)
    raise RuntimeError("RabbitMQ unreachable")

def worker():
    conn = connect()
    channel = conn.channel()
    channel.queue_declare(queue='router_jobs')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='router_jobs',
                      auto_ack=True,
                      on_message_callback=callback)
    
    channel.start_consuming()


if __name__ == "__main__":
    try:
        worker()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)