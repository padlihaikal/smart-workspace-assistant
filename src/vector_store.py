from config.config import CHROMA_PATH
import chromadb

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    response = client.get_or_create_collection("documents")

    return response
    

def add_chunks(user_id: int, document_id: int, file_name: str, chunks: list[str]) -> None:
    if not chunks:
        return
    
    collection = get_collection()

    for i, chunk in enumerate(chunks):
        chunk_id = f"{document_id}_{i}"
        metadata = {
            "user_id": user_id,
            "document_id": document_id,
            "file_name": file_name
            }
        
        collection.upsert(
            ids=[chunk_id],
            documents=[chunk],
            metadatas=[metadata]
        )