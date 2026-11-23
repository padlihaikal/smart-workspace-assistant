import os
from src.vector_store import search_chunks
from src.llm import build_context, generate_answer

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
    ),
    4: (
        "password-policy.txt",
        "Usernames are registered in the database. Passwords must contain at least three special characters."
    ),
    5: (
        "claim-travel-expense.txt",
        "Employees can submit travel expense claims whitin seven days of their trip."
    ),
    6: (
        "remote-policy.txt",
        "Staff must online for at least eight hours per day."
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

def run_evaluation():
    retrieval_hits = 0
    answer_hits = 0

    for test_case in CASES:
        question, keyword, expected_file = test_case
        chunks = search_chunks(EVAL_USER_ID, question, 3)

        file_found = False
        answer_found = False
        
        for chunk in chunks:
            chunk_result = chunk["file_name"]

            if chunk_result == expected_file:
                retrieval_hits += 1
                file_found = True
                break

        if not chunks:
             pass
        else:   
            answer = generate_answer(question, build_context(chunks))
            if keyword.lower() in answer.lower():
                answer_hits += 1
                answer_found = True
        print(f"{question}, {file_found}, {answer_found}")
    
    print(f"Retrieval:{retrieval_hits}/3\n\nAnswer:{answer_hits}/3")

if __name__ == "__main__":
    index_documents()
    run_evaluation()