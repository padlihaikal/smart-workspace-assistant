from pydantic import BaseModel

class TaskRequest(BaseModel):
    title: str

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

class UserRequest(BaseModel):
    username: str
    password: str
    email: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str