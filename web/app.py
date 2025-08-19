from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

sample = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
mydb = client["ipa2025"]
mycol = mydb["routers"]
print(client.list_database_names())

data = []

@sample.route("/")
def main():
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        data.append({"ip": ip, "username": username})
        router = {
            "ip": ip,
            "username":username,
            "password":password
        }
        mycol.insert_one(router)
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        if 0 <= idx < len(data):
            data.pop(idx)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)