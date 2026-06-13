from sqlalchemy.orm import Session
from src.users.models import UserModel
from fastapi import HTTPException,status,Depends
from src.utils.db import get_db
from pwdlib import PasswordHash
from src.utils.redis import redis_client
import jwt
import uuid
from jwt.exceptions import InvalidTokenError
from jwt import ExpiredSignatureError

from fastapi import Request
from src.utils.settings import settings
password_hash = PasswordHash.recommended()
EXP_TIME = 30

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        token = token.split(" ")[-1]

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = data.get("_id")

        user = db.get(UserModel, uuid.UUID(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unauthorized"
            )

        # --------------------------
        # REDIS SESSION CHECK
        # --------------------------

        session_token = redis_client.get(
            f"session:{user.id}"
        )

        if not session_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired. Please login again."
            )

        if session_token != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session"
            )

        # Refresh inactivity timer
        redis_client.expire(
            f"session:{user.id}",
            1800
        )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )