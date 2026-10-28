from sqlalchemy import create_engine, String, Boolean, ForeignKey, select, Text, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from passlib.context import CryptContext
from datetime import datetime, timezone
from config.config import DATABASE_URL

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed : Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=True)

def create_user(username, password, email):
    db = SessionLocal()
    try:
        hashed_password = pwd_context.hash(password)

        new_user = User(
            username=username,
            password=hashed_password,
            email=email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    finally:
        db.close()

def get_user(username):
    db = SessionLocal()
    try:

        stmt = select(User).where(User.username == username)
        user = db.scalars(stmt).first()
        return user
    finally:
        db.close()
    

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_task(title, user_id):
    db = SessionLocal()

    try:
        new_task = Task(
            title=title,
            completed=False,
            user_id=user_id
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    finally:
        db.close()

def create_document(file_name, content_type, text, user_id):
    db = SessionLocal()

    try:
        document = Document(
            file_name=file_name,
            content_type=content_type,
            text=text,
            user_id=user_id
        )

        db.add(document)
        db.commit()
        db.refresh(document)
        return document
    finally:
        db.close()
    
def get_all_tasks(user_id):
    db = SessionLocal()
    try:
        stmt = select(Task).where(Task.user_id == user_id)
        result = db.scalars(stmt)
        tasks = result.all()
        return tasks
    finally:
        db.close()  

def get_task(task_id):
    db = SessionLocal()
    try:

        stmt = select(Task).where(Task.id == task_id)
        result = db.scalars(stmt)
        task = result.first()
        return task
    finally:
        db.close()

def update_task(task_id, title):
    db = SessionLocal()
    try:
        stmt = select(Task).where(Task.id == task_id)
        task = db.scalars(stmt).first()

        if task is None:
            return None
    
        task.title = title

        db.commit()
        return task
    finally:
        db.close()

def delete_task(task_id):
    db = SessionLocal()
    try:

        stmt = select(Task).where(Task.id == task_id)
        task = db.scalars(stmt).first()

        if task is None:
            return None

        db.delete(task)
        db.commit()
        return task
    finally:
        db.close()