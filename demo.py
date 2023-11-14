from json import loads
from random import randint

import requests
from faker import Faker

target_create_domain = "http://127.0.0.1:8000/"

fake = Faker()


# Adding patients
def call(json, endpoint="create"):
    try:
        resp = requests.post(target_create_domain + endpoint, json=json).text
        return loads(resp)
    except requests.exceptions.ConnectionError:
        print("Are you sure the flask web server is running?")
        exit()


for i in range(10):
    call(
        {
            "c": "patients",
            "data": {
                "name": fake.name(),
                "age": randint(18, 90),
                "date": f"{randint(2010,2023)}-{randint(1,12)}-{randint(1,28)}",
            },
        }
    )
    u_id = call(
        {
            "c": "doctors",
            "data": {
                "name": fake.name(),
                "age": randint(18, 90),
                "exp": randint(1, 30),
                "fees": randint(100, 3000),
            },
        }
    )["u_id"]
    print(f"Wrote {u_id} to firebase database")
    print(f"Fetching {u_id} details....")
    print(
        call(
            {
                "c": "doctors",
                "u_id": u_id,
            },
            "fetch",
        )
    )
    print("DONE\n\n")
