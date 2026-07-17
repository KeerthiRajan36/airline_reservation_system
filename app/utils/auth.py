from jose import JWTError
from jose import jwt

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.config import settings
from app.database.database import get_db
from app.models.user import User


security = HTTPBearer()


def get_current_user(
        credential: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid Authentication"
    )

    token = credential.credentials
    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user