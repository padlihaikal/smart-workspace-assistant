import os

os.environ["CHROMA_PATH"] = "chroma_db_eval"

EVAL_USER_ID = 1

from src.processing import chunk_text
from src.vector_store import add_chunks

DOCUMENTS = {
    1: (
        "return-policy.txt",
        "Customers can return purchased items within 14 days of delivery."
    ),
    2: (
        "working-hours.txt",
        "The office operates from 09:00 to 17:00, Monday through Friday."
    ),
    3: (
        "leave-policy.txt",
        "Employees are entitled to 20 days of annual leave per year."
    )
}

CASES = [
    (
        "How many days do customers have to return purchased items?",
        "14 days",
        "return-policy.txt"
    ),
    (
        "What are the office operating hours?",
        "09:00",
        "working-hours.txt"
    ),
    (
        "How many days of annual leave are employees entitled to?",
        "20 days",
        "leave-policy.txt"
    )
]

def index_documents():
    for document_id, (file_name, text) in DOCUMENTS.items():
        chunks = chunk_text(text)
        add_chunks(EVAL_USER_ID, document_id, file_name, chunks)