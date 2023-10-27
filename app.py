from os import getenv

from dotenv import load_dotenv
from flask import Flask

from db import initialise_db

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


if __name__ == "__main__":
    """
    Set the database up
    """
    initialise_db()

    port: int = int(getenv("PORT")) if getenv("PORT") else 8000
    debug = True if str(getenv("DEBUG")).casefold() == "true" else False
    app.run(host="0.0.0.0", port=port, debug=debug)
