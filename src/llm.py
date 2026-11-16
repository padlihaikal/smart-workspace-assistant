def build_context(chunks: list[dict]) -> str:
    texts = []

    for i, chunk in enumerate(chunks, start=1):
        
        text = f"[{i}] {chunk['file_name']}: {chunk['text']}"

        texts.append(text)
    return "\n\n".join(texts)
