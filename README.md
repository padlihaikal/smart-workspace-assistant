# Smart Workspace Assistant

## Description

Smart Workspace Assistant is a Python-based project that started as a simple Command Line Interface (CLI) application and was later developed into a backend REST API.

Version 1.0 focused on practicing Software Engineering fundamentals such as file management, JSON, exception handling, logging, clean code, Git, and CLI application development.

Version 2.0 extends the project by using FastAPI and SQLite. The API provides basic CRUD operations for task management and connects the application to a SQLite database.

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

Version 2.0 extends the previous CLI application into a backend REST API using FastAPI and SQLite.

Main features:

- REST API
- HTTP methods
- Request and response handling
- Pydantic validation
- Create task
- Get all tasks
- Get task by ID
- Update task
- Delete task
- SQLite database integration
- HTTP error handling
- API testing using Swagger UI

Technologies:

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn

## Project Structure

```text
smart-workspace-assistant/
    config/
    data/
    logs/
    reports/
    src/
        __init__.py
        main.py
        database.py
    .gitignore
    README.md
    requirements.txt
```
## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Start the FastAPI application using Uvicorn:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

- `GET /` - Get API information
- `GET /about` - Get project information
- `GET /search` - Search endpoint example
- `POST /tasks` - Create a task
- `GET /tasks` - Get all tasks
- `GET /tasks/{task_id}` - Get a task by ID
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Database

Version 2.0 uses SQLite to store task data.

The database contains a `tasks` table with:

- `id`
- `title`

The database operations are implemented in:

```text
src/database.py
```

The FastAPI application is implemented in:

```text
src/main.py
```

The local SQLite database file is excluded from Git using `.gitignore`.

## Testing

The API was tested using Swagger UI.

The following operations were tested:

- Create a task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task
- Get a deleted task and receive a 404 Not Found response

These tests confirmed that the FastAPI application is connected to the SQLite database and that the basic CRUD operations work correctly.

## Screenshot

Swagger UI was used to test the API during development.

Screenshots can be added to this section in future updates.

## Future Development

Possible future improvements include:

- PostgreSQL
- SQLAlchemy
- Alembic
- Authentication
- Environment variables
- Integration with AI applications

## Author

Muhamad Padli Haikal