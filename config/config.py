from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")