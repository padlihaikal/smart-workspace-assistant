import os
from dotenv import load_dotenv

load_dotenv()

test_database_url = os.getenv("TEST_DATABASE_URL")

if not test_database_url:
    raise ValueError("TEST_DATABASE_URL belum diatur di .env")

if not test_database_url.endswith("_test"):
    raise ValueError("nama database test harus berakhiran _test")

os.environ["DATABASE_URL"] = test_database_url
