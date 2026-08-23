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
    alembic/              # Database migrations
    config/
        config.py         # Loads environment variables
    src/
        __init__.py
        main.py            # FastAPI app and endpoints
        database.py         # SQLAlchemy models and queries
        schemas.py           # Pydantic request/response models
        auth.py               # JWT authentication logic
    tests/
        test_main.py          # pytest test suite
    conftest.py
    alembic.ini
    .gitignore
    .env                       # Not committed (see .gitignore)
    README.md
    requirements.txt
```

## Installation

Create a virtual environment:

```
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```
pip install -r requirements.txt
```

Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost/smart_workspace
SECRET_KEY=your-secret-key-here
```

Run database migrations:

```
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
3. Server verifies the password and returns a JWT access token
4. Client sends the token in the `Authorization: Bearer <token>` header
5. Protected endpoints validate the token via `Depends(get_current_user)`
6. The authenticated user's identity is used to enforce task ownership

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

```
pytest
```

Tests cover:

- Public endpoint access
- Rejecting unauthenticated requests to protected endpoints
- Full registration → login → authenticated request flow
- Duplicate username registration returning `409 Conflict`

## Future Improvement

- Implement the `/search` endpoint to actually filter tasks by keyword
- Add JWT token expiration
- Add pagination for `GET /tasks`
- Add refresh tokens
- Expand test coverage (404, PUT, DELETE flows)
- Deploy to a cloud environment
- Integration with AI applications / AI agents

## Author

Muhamad Padli Haikal

## License

MIT License
