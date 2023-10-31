from os import path
from sqlite3 import connect
from typing import Any, Optional
from uuid import uuid4
from os import getenv
from dotenv import load_dotenv

from firebase_admin import credentials, firestore, initialize_app

from security import enc_class

db_name = "healthcare.db"
script_dir = path.dirname(__file__)
db_path = path.join(script_dir, db_name)

load_dotenv()

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


all_tables = [
    patients_table,
    doctors_table,
    ailments_table,
    medicines_table,
    consultation_table,
]

primary_keys = {
    patients_table: patients_primary_key,
    doctors_table: doctors_primary_key,
    ailments_table: ailments_primary_key,
    medicines_table: medicines_primary_key,
    consultation_table: consultation_primary_key,
}


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


class FirestoreWrapper:
    def __init__(self, creds_path: str):
        creds = credentials.Certificate(creds_path)
        initialize_app(creds)
        self.client = firestore.client(app=None)

    def create(self, collection_name: str, document_id: str, document_dict: dict):
        doc_ref = self.client.collection(collection_name).document(document_id)
        doc_ref.set(document_dict)

    def update(self, collection_name: str, document_id: str, document_dict: dict):
        doc_ref = self.client.collection(collection_name).document(document_id)
        doc_ref.update(document_dict)

    def delete(self, collection_name: str, document_id: str):
        doc_ref = self.client.collection(collection_name).document(document_id)
        doc_ref.delete()

    def fetch(self, collection_name: str, document_id: str):
        doc_ref = self.client.collection(collection_name).document(document_id)
        return doc_ref.get().to_dict()


class DBWrapper:
    def __init__(self):
        self.firestore = FirestoreWrapper("./" + getenv("FIREBASE_CREDS_FILE"))

        self.db: SqliteWrapper = SqliteWrapper(db_path)
        ...

    def update(self, table_name, key):
        self.firestore.update


MasterDB = DBWrapper()

default_queries = [
    f"""CREATE TABLE IF NOT EXISTS {patients_table} ({patients_primary_key} TEXT NOT NULL PRIMARY KEY, patient_name TEXT NOT NULL, age TEXT NOT NULL, first_consulation_date TEXT NOT NULL)""",
    f"""CREATE TABLE IF NOT EXISTS {doctors_table} ({doctors_primary_key} TEXT NOT NULL PRIMARY KEY, doctor_name TEXT NOT NULL, experience TEXT)""",
    f"""CREATE TABLE IF NOT EXISTS {ailments_table} ({ailments_primary_key} TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, description TEXT, medicines TEXT)""",
    f"""CREATE TABLE IF NOT EXISTS {medicines_table} ({medicines_primary_key} TEXT NOT NULL PRIMARY KEY, cart_items TEXT NOT NULL, COST TEXT NOT NULL)""",
    f"""CREATE TABLE IF NOT EXISTS {consultation_table} ({consultation_primary_key} TEXT NOT NULL PRIMARY KEY, patient_id TEXT NOT NULL, doctor_id TEXT NOT NULL, ailments_ids TEXT NOT NULL)""",
]


def check_record(table_name: str, p_key: str, p_value: str) -> bool:
    return db.exists_perhaps(table_name, p_key, p_value)


def check_if_patient_exists(patient_id: str) -> bool:
    return db.exists_perhaps(patients_table, patients_primary_key, patient_id)


def create_patient(
    patient_name: str,
    patient_age: int,
    patient_first_consultation_date: str,
) -> bool:
    """
    Create a patient by checking if it already exists
    """
    patient_id = uuid4()
    if not check_if_patient_exists(patient_id):
        query = f"""INSERT INTO {patients_table} VALUES (?,?,?,?)"""
        db.execute(
            query,
            patient_id,
            patient_name,
            patient_age,
            patient_first_consultation_date,
        )
        return True
    else:
        return create_patient(
            patient_name, patient_age, patient_first_consultation_date
        )
    return False


def fetch_patient_details(patient_id: str):
    """
    Returns the details of the patient from he db.
    """

    return db.fetchone(
        f"""SELECT * FROM {patients_table} WHERE {patients_primary_key}=?""", patient_id
    )


def check_if_doctor_exists(doctor_id: str) -> bool:
    return db.exists_perhaps(doctors_table, doctors_primary_key, doctor_id)


def create_doctor(doctor_id: str, doctor_name: str, doctor_exp: int) -> bool:
    if not check_if_doctor_exists(doctor_id):
        query = f"""INSERT INTO {doctors_table} VALUES (?,?,?)"""
        db.execute(query, doctor_id, doctor_name, doctor_exp)
        return True
    return False


def fetch_doctor_details(doctor_id: str):
    """
    Returns he detais of the doctor from the db
    """
    return db.fetchone(
        f"""SELECT * FROM {doctors_table} WHERE {doctors_primary_key}=?""", doctor_id
    )


def initialise_db():
    """
    Create database if it doesn't exist. Run default queries which will create the necessary tables
    """
    for query in default_queries:
        db.execute(query)


initialise_db()
