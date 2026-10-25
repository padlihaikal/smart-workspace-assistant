# Smart Workspace Assistant

## Description

Smart Workspace Assistant is a Python-based project that started as a simple Command Line Interface (CLI) application and was later developed into a backend REST API.

Version 1.0 focused on practicing Software Engineering fundamentals such as file management, JSON, exception handling, logging, clean code, Git, and CLI application development.

Version 2.0 extends the project into a REST API backend built with FastAPI, PostgreSQL, and JWT authentication, developed as a learning project to practice backend engineering fundamentals. Each user can only access their own tasks, enforced through ownership checks at the API level. This backend is designed to later serve as the foundation for AI-powered applications.

## Version 1.0 - CLI

Version 1.0 was developed as a Command Line Interface application.

Main features:

- CLI commands
- Read and save task data using JSON
- File management
- Exception handling
- Logging
- Clean code

Technologies:

- Python
- JSON
- Git
- GitHub
- Virtual Environment
- requirements.txt

## Version 2.0 - REST API

Version 2.0 rebuilds the project as a backend REST API using FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication.

Main features:

- REST API with FastAPI
- User registration and login
- Password hashing with bcrypt
- JWT-based authentication (OAuth2PasswordBearer)
- Protected endpoints using `Depends`
- Task CRUD (Create, Read, Update, Delete)
- Task ownership: each task belongs to a user, enforced with a foreign key
- Authorization checks: users can only access their own tasks (401 / 403 / 404 handling)
- Database migrations with Alembic
- Environment variables for configuration (`.env`)
- Centralized error handling, including a global exception handler
- Automated testing with pytest
- Auto-generated API documentation via Swagger UI

Technologies:

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic
- python-jose (JWT)
- passlib + bcrypt (password hashing)
- python-dotenv
- pytest + httpx (testing)
- Uvicorn

## Project Structure

```
smart-workspace-assistant/
├── alembic/                  # Database migrations
├── config/
│   └── config.py             # Loads environment variables
├── src/
│   ├── __init__.py
│   ├── main.py               # FastAPI app and endpoints
│   ├── database.py           # SQLAlchemy models and queries
│   ├── schemas.py            # Pydantic request/response models
│   └── auth.py               # JWT authentication logic
├── tests/
│   ├── test_main.py          # pytest test suite
│   └── conftest.py
├── alembic.ini
├── .gitignore
├── .env                      # Not committed (see .gitignore)
├── .env.example
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root using `.env.example` as a template. Configure the following variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:your-password-here@localhost/smart_workspace
TEST_DATABASE_URL=postgresql+psycopg://postgres:your-password-here@localhost:5432/smart_workspace_test
SECRET_KEY=your-secret-key-here
```

Replace the placeholder values with your local database credentials and a secure secret key. Do not commit real passwords or secrets to version control.

Run database migrations:

```powershell
alembic upgrade head
```

## How to Run

Start the FastAPI application using Uvicorn:

```
uvicorn src.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|--------------|----------------|
| GET | `/` | API root info | No |
| GET | `/about` | Project info | No |
| POST | `/users` | Register a new user | No |
| POST | `/login` | Login and receive a JWT token | No |
| POST | `/tasks` | Create a task | Yes |
| GET | `/tasks` | Get all tasks owned by the current user | Yes |
| GET | `/tasks/{task_id}` | Get a task by ID (owner only) | Yes |
| PUT | `/tasks/{task_id}` | Update a task (owner only) | Yes |
| DELETE | `/tasks/{task_id}` | Delete a task (owner only) | Yes |
| GET | `/search` | Search endpoint (in progress) | No |

## Database

Version 2.0 uses PostgreSQL, managed through SQLAlchemy ORM and versioned with Alembic migrations.

**users** table:
- `id`
- `username` (unique)
- `password` (hashed with bcrypt)
- `email`

**tasks** table:
- `id`
- `title`
- `completed`
- `user_id` (foreign key referencing `users.id`)

Each task belongs to exactly one user. Ownership is enforced at the API layer, not just the database layer.

## Authentication

Authentication uses JWT (JSON Web Token) with the OAuth2 password flow:

1. User registers via `POST /users`
2. User logs in via `POST /login` with username and password
3. Server verifies the password and returns a JWT access token valid for 30 minutes.
4. Client sends the token in the `Authorization: Bearer <token>` header.
5. Protected endpoints validate the token via `Depends(get_current_user)`.
6. The authenticated user's identity is used to enforce task ownership.

## Error Handling

The API returns explicit HTTP status codes instead of leaking raw internal errors:

- `401 Unauthorized` — missing or invalid authentication token
- `403 Forbidden` — authenticated, but not the owner of the requested resource
- `404 Not Found` — requested resource does not exist
- `409 Conflict` — username already exists during registration
- `500 Internal Server Error` — caught by a global exception handler, returns a generic safe message

## Testing

Automated tests are written with `pytest` and FastAPI's `TestClient`.

Run the test suite:

```bash
pytest
```

Tests cover:

- Public endpoint access
- Rejecting unauthenticated requests to protected endpoints
- Full registration → login → authenticated request flow
- Duplicate username registration returning `409 Conflict`
- Expired JWT access tokens returning `401 Unauthorized`

### Separate Test Database

Tests use a separate PostgreSQL database named `smart_workspace_test`. The test database name must end with `_test` to help prevent tests from running against the development database.

### Test Database Setup

Before running tests, create the test database and run `alembic upgrade head` with `DATABASE_URL` pointing to the test database. Set `TEST_DATABASE_URL` in the `.env` file to the test database connection URL.

## Future Improvement

- Implement the `/search` endpoint to actually filter tasks by keyword
- Add pagination for `GET /tasks`
- Add refresh tokens
- Expand test coverage (404, PUT, DELETE flows)
- Deploy to a cloud environment
- Integration with AI applications / AI agents

## Author

Muhamad Padli Haikal

## License

MIT License
