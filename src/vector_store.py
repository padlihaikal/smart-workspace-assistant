from config.config import CHROMA_PATH

def get_collection():
    import chromadb
    
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

def search_chunks(user_id: int, query: str, n_results: int = 3) -> list[dict]:
    results = get_collection().query(
        query_texts=[query],
        n_results=n_results,
        where={"user_id": user_id}
    )
    chunks_list = []

    for result in zip (results["documents"][0], results["metadatas"][0], results["distances"][0]):
        chunk_text, metadata, distance = result
        
        chunk = {
           "text": chunk_text,
           "file_name": metadata["file_name"],
           "document_id": metadata["document_id"],
           "distance": distance 
       }
        chunks_list.append(chunk)
    return chunks_list