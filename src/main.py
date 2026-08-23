from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Form,
    Depends
    )
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.database import (
    create_task,
    get_all_tasks, 
    get_task, 
    update_task, 
    delete_task,
    create_user,
    verify_password,
    get_user
    )
from src.schemas import (
    TaskRequest,
    TaskResponse,
    UserRequest,
    UserResponse,
)
from src.auth import(
    create_access_token,
    get_current_user
)

app = FastAPI(
    title="Smart Workspace Assistant API",
    description="REST API untuk mengelola task per-user, dengan autentikasi JWT.",
    version="2.0.0"
)

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail":"Something went wrong. Please try again later."}
    )

@app.get("/")
def root():
    """Endpoint dasar untuk mengecek API berjalan."""
    return{
        "message":"Smart Workspace Assistant API"
}

@app.get("/about")
def about():
    """Menampilkan info nama dan versi API."""
    return{
        "project": "Smart Workspace Assistant API",
        "version": "2.0.0"
    }

@app.post("/users", response_model=UserResponse)
def create_user_endpoint(user_request: UserRequest):
    """Daftarkan user baru dengan username unik."""
    try:
        user = create_user(
            user_request.username,
            user_request.password,
            user_request.email
        )
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

@app.post("/login")
def login(username: str = Form(),
          password : str = Form()):
    """Login user dan menghasilkan JWT access token."""
    user = get_user(username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int, current_user = Depends(get_current_user)):
    """Ambil detail satu task berdasarkan ID, jika milik user yang login."""
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this task"
        )
    return task

@app.get("/search")
def search(keyword:str):
    """Endpoint pencarian (Masih dalam pengembangan)."""
    return{
        "keyword": keyword
    }

@app.post("/tasks", response_model=TaskResponse)
def create_task_endpoint(task_request:TaskRequest, current_user = Depends(get_current_user)):
    """Buat task baru untuk user yang sedang login."""
    task = create_task(task_request.title, current_user.id)
    return task

@app.get("/tasks", response_model=list[TaskResponse])
def get_all_task_endpoint(current_user = Depends(get_current_user)):
    """Ambil semua task milik user yang sedang login."""
    return get_all_tasks(current_user.id)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task_request:TaskRequest, current_user = Depends(get_current_user)):
    """Perbarui judul task, hanya jika milik user yang login."""
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this task"
        )
    updated_task = update_task(task_id, task_request.title)
    return updated_task

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task_endpoint(task_id: int, current_user = Depends(get_current_user)):
    """Hapus task, hanya jika milik user yang login."""
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code = 404,
            detail = "Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this task"
        )

    deleted_task = delete_task(task_id)

    return deleted_task