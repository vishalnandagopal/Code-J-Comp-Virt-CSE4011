from os import getenv

from dotenv import load_dotenv
from flask import Flask, request

from db import all_tables, initialise_db, update_record, create_record, delete_record

load_dotenv()

app: Flask = Flask("Virtualisation J-Component")


@app.route("/welcome", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def welcome():
    return "Welcome to a secure, compliant &  containerized storage solution for healthcare providers"


@app.route("/schema", methods=["POST"])
def schema():
    ...


@app.route("/post", methods=["POST"])
def post():
    ...


@app.route("/update", methods=["POST"])
def update():
    if request.is_json:
        data = request.get_json()
        if "table" not in data or data["table"] not in all_tables:
            return "Mention proper table name", 400
        if "p_key" in data:
            p_key = data["p_key"]
            update_record(data["table"], p_key, data)
    return "Invalid JSON", 400


@app.route("/fetch", methods=["POST"])
def fetch():
    ...


if __name__ == "__main__":
    port: int = int(getenv("PORT")) if getenv("PORT") else 8000
    debug = True if str(getenv("DEBUG")).casefold() == "true" else False
    app.run(host="0.0.0.0", port=port, debug=debug)
