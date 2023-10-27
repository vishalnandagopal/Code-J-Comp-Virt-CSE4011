import sqlite3

from json import dumps as jsondumps
from json import load as jsonload
from json import loads as jsonloads
from os import path
from sqlite3 import connect
from typing import Any, Optional
from uuid import uuid4

from miscellaneous import hasher

db_name = "healthcare.db"
script_dir = path.dirname(__file__)
db_path = path.join(script_dir, db_name)

patients_table = "patients"
doctors_table = "doctors"
ailments_table = "ailments"
medicines_table = "medicines"
consultation_table = "consultations"


patients_primary_key = "patient_id"
doctors_primary_key = "doctor_id"
ailments_primary_key = "ailment_id"
medicines_primary_key = "medicine_id"
consultation_primary_key = "consultation_id"


class SqliteWrapper:
    def __init__(
        self,
        path: str,
    ):
        self.db = connect(path, check_same_thread=False)

    def execute(self, query: str, *params):
        cur = self.db.cursor()
        cur.execute(query, params)
        self.db.commit()
        cur.close()

    def fetchone(self, query: str, *params) -> Optional[Any]:
        cur = self.db.cursor()
        res = cur.execute(query, params)
        data = res.fetchone()
        cur.close()
        return data

    def fetchall(self, query: str, *params) -> list[Any]:
        cur = self.db.cursor()
        res = cur.execute(query, params)
        data = res.fetchall()
        cur.close()
        return data

    def view_all(self, table_name: str) -> list[Any]:
        return self.fetchall(f"""SELECT * FROM {table_name}""")

    def insert(self, table_name: str, values: list[str]):
        self.execute(
            f"""INSERT INTO {table_name} 
            VALUES ({"?,"*len(values)})""",
            (values),
        )

    def exists_perhaps(self, table_name: str, key: str, key_value: str) -> bool:
        return bool(
            self.fetchall(f"""SELECT * FROM {table_name} WHERE {key}=?""", key_value)
        )

    def get(self, table: str, key_name: str, key_value: str) -> list:
        return self.fetchone(f'SELECT * FROM {table} WHERE {key_name}="{key_value}"')


db: SqliteWrapper = SqliteWrapper(db_path)

default_queries = [
    f"""CREATE TABLE IF NOT EXISTS {patients_table} ({patients_primary_key} TEXT NOT NULL PRIMARY KEY, patient_name TEXT NOT NULL, age int NOT NULL, first_consulation_date DATE NOT NULL)""",
    f"""CREATE TABLE IF NOT EXISTS {doctors_table} ({doctors_primary_key} TEXT NOT NULL PRIMARY KEY, doctor_name TEXT NOT NULL, experience INT)""",
    f"""CREATE TABLE IF NOT EXISTS {ailments_table} ({ailments_primary_key} TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, description TEXT, medicines TEXT)""",
    f"""CREATE TABLE IF NOT EXISTS {medicines_table} ({medicines_primary_key} TEXT NOT NULL PRIMARY KEY, cart_items TEXT NOT NULL)""",
    f"""CREATE TABLE IF NOT EXISTS {consultation_table} ({consultation_primary_key} TEXT NOT NULL PRIMARY KEY, patient_id TEXT NOT NULL, doctor_id TEXT NOT NULL, ailments_ids TEXT NOT NULL)""",
]


def check_if_patient_exists(patient_id: str) -> bool:
    return db.exists_perhaps(patients_table, patients_primary_key, patient_id)


def create_patient(
    patient_id: str,
    patient_name: str,
    patient_age: int,
    patient_first_consultation_date: str,
) -> bool:
    """
    Create a user by passing his username, password and type. Checks if the user already exists or not before creating one. Returns true if user has been created succesfully, false if user already exists or if create operation fails.
    """

    if not check_if_patient_exists(patients_table, patients_primary_key, patient_id):
        query = f"""INSERT INTO {patients_table} VALUES (?,?,?,?)"""
        db.execute(
            query,
            patient_id,
            patient_name,
            patient_age,
            patient_first_consultation_date,
        )
        return True
    return False


def fetch_patient_details(patient_id: str):
    """
    Returns the details of the patient fromt he db.
    """
    return db.fetchone(
        f"""SELECT * FROM {patients_table} WHERE {patients_primary_key}=?""", patient_id
    )


def initialise_db():
    """
    Create database if it doesn't exist. Run default queries which will create the necessary tables
    """
    for query in default_queries:
        db.execute(query)
