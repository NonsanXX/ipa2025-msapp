import os
from datetime import datetime

from pymongo import MongoClient



def get_router_info():
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    routers = db["routers"]

    router_data = routers.find()
    return router_data

def save_router_interfaces(ip, interfaces):
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    routers = db["interface_status"]
    if interfaces:
        routers.insert_one({
                "router_ip": ip,
                "timestamp": datetime.now(),
                "interfaces": interfaces
            })
    else:
        print("Invalid Interfaces list!")
        return

if __name__=='__main__':
    get_router_info()