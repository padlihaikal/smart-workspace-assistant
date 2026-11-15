from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

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

class DocumentResponse(BaseModel):
    id: int
    file_name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AskRequest(BaseModel):
    question: str = Field(min_length=1)

class Source(BaseModel):
    file_name: str
    document_id: int

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]