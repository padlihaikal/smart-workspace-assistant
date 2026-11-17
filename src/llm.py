from openai import OpenAI
from config.config import GROQ_API_KEY

MODEL = "openai/gpt-oss-20b"
BASE_URL = "https://api.groq.com/openai/v1"
SYSTEM_PROMPT = (
    "ANSWER ONLY USING THE PROVIDED CONTEXT."
    "CITE SOURCES USING THEIR NUMBERS, FOR EXAMPLE [1]."
    "IF THE ANSWER IS NOT AVAILABLE IN THE CONTEXT, SAY: I don't know based on your documents."
)

def build_context(chunks: list[dict]) -> str:
    texts = []

    for i, chunk in enumerate(chunks, start=1):
        
        text = f"[{i}] {chunk['file_name']}: {chunk['text']}"

        texts.append(text)
    return "\n\n".join(texts)

def get_client():
    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=BASE_URL,
        timeout=30
    )

def generate_answer(question: str, context: str) -> str:
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    )
    return response.choices[0].message.content
