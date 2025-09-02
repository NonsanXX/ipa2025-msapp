import os
import ntc_templates
from netmiko import ConnectHandler


def get_interfaces(host, username, password):
    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )
    router = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
    }
    try:
        with ConnectHandler(**router) as net_connect:
            # print(f"Successfully connect to {host}")
            output = net_connect.send_command("show ip int br", use_textfsm=True)
            return output
    except Exception as e:
        print("Failed to Connect!:", e)
