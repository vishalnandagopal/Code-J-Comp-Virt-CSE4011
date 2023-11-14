from os import getenv

from dotenv import load_dotenv
from flask import Flask, request

from database import check_collection, check_document_id, db

load_dotenv()

app: Flask = Flask("Virtualisation J-Component")


@app.route("/welcome", methods=["GET", "POST"])
@app.route("/hello", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    print("welcome to this app")
    return {
        "msg": "Welcome to a secure, compliant & containerized storage solution for healthcare providers"
    }, 200


@app.route("/create", methods=["POST"])
def create():
    d = request.get_json()
    if not check_collection(d["c"]):
        return {"msg": "Invalid collection name"}, 400
    u_id = db.create(d["c"], d["data"])
    return {"msg": "Success", "u_id": u_id}, 200


@app.route("/update", methods=["POST"])
def update():
    d = request.get_json()
    if not check_document_id(d["c"], d["u_id"]):
        return {"msg": "Invalid document ID or collection name"}, 400
    return db.update(d["c"], d["u_id"], d["data"])


@app.route("/fetch", methods=["POST"])
def fetch():
    d = request.get_json()
    if not check_document_id(d["c"], d["u_id"]):
        return {"msg": "Invalid document ID or collection name"}, 400
    return db.fetch(d["c"], d["u_id"])


@app.route("/delete", methods=["POST"])
def delete():
    d = request.get_json()
    if not check_document_id(d["c"], d["u_id"]):
        return {"msg": "Invalid document ID or collection name"}, 400
    return db.delete(d["c"], d["u_id"])


if __name__ == "__main__":
    port: int = int(getenv("PORT")) if getenv("PORT") else 8000
    debug = True if str(getenv("DEBUG")).casefold() == "true" else False
    app.run(host="0.0.0.0", port=port, debug=debug)
