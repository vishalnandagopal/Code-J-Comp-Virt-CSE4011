from os import getenv, path
from uuid import uuid4

from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app

from security import get_encryptor

load_dotenv()

patients_collection = "patients"
doctors_collection = "doctors"
ailments_collection = "ailments"
medicines_collection = "medicines"
consultation_collection = "consultations"


all_collections = [
    patients_collection,
    doctors_collection,
    ailments_collection,
    medicines_collection,
    consultation_collection,
]


def check_collection(collection_name: str) -> bool:
    if collection_name not in all_collections:
        print("Seems like you have asked to modify a non-existant collection/table")
        return False
    else:
        return True


def check_document_id(collection_name: str, document_id: str) -> bool:
    if not check_collection(collection_name):
        return False
    if db.check_if_exists(collection_name, document_id):
        return True
    return False


class FirestoreWrapper:
    def __init__(self, creds_path: str):
        creds = credentials.Certificate(creds_path)
        initialize_app(creds)
        self.client = firestore.client(app=None)
        self.encryptor = get_encryptor()

    def create(self, collection_name: str, document_dict: dict) -> str:
        u_id = str(uuid4())
        doc_ref = self.client.collection(collection_name).document(u_id)
        print(f"Added {document_dict}")
        doc_ref.set(self.encrypt(document_dict))
        return u_id

    def update(
        self, collection_name: str, document_id: str, document_dict: dict
    ) -> bool:
        doc_ref = self.client.collection(collection_name).document(document_id)
        doc_ref.update(self.encrypt(document_dict))
        return True

    def delete(self, collection_name: str, document_id: str):
        doc_ref = self.client.collection(collection_name).document(document_id)
        if not doc_ref.get().to_dict():
            return False
        doc_ref.delete()
        return True

    def fetch(self, collection_name: str, document_id: str) -> dict:
        doc_ref = self.client.collection(collection_name).document(document_id)
        return self.decrypt(doc_ref.get().to_dict())

    def fetch_all(self, collection_name: str) -> dict:
        docs = self.client.collection(collection_name).stream()
        for doc in docs:
            print(f"{doc.id} => {self.decrypt(doc.to_dict())}")

    def check_if_exists(self, collection_name: str, document_id: str) -> bool:
        return bool(self.fetch(collection_name, document_id))

    def encrypt(self, data: dict):
        for key in data:
            data[key] = self.encryptor.encrypt(data[key])
        return data

    def decrypt(self, data: dict):
        for key in data:
            data[key] = self.encryptor.decrypt(data[key])
        return data


def initialise_db():
    """
    Create database if it doesn't exist. Run default queries which will create the necessary tables
    """
    db = FirestoreWrapper("./" + getenv("FIREBASE_CREDS_FILE"))
    return db


db = initialise_db()
