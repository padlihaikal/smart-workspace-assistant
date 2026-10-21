from fastapi import (
    HTTPException,
    Depends)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    jwt,
    JWTError)
from src.database import get_user
from config.config import SECRET_KEY
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(username: str):
    to_encode = {"sub": username}

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = get_user(username)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )