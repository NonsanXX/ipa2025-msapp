import json
from router_client import get_interfaces
from database import save_router_interfaces


def callback(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    ip = data["ip"]
    usr = data["username"]
    pwd = data["password"]

    print(f"Received job for router {ip}")
    output = get_interfaces(ip, usr, pwd)
    print(json.dumps(output, indent=2))

    save_router_interfaces(ip, output)
    print(f"Stored interface status for {ip}")
