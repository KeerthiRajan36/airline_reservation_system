from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth_schema import RegisterRequest
from app.schemas.auth_schema import LoginRequest
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
)

from app.utils.hashing import Hash
from app.utils.jwt import create_access_token


class AuthService:

    @staticmethod
    def register(db: Session, request: RegisterRequest):

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise UserAlreadyExistsException()

        user = User(
            name=request.name,
            email=request.email,
            password=Hash.hash_password(request.password),
            role="Passenger",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "Registration Successful",
            "user": user,
        }

    @staticmethod
    def login(db: Session, request: LoginRequest):

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if not user:
            raise InvalidCredentialsException()

        if not Hash.verify_password(
            request.password,
            user.password,
        ):
            raise InvalidCredentialsException()

        token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
            }
        )

        return {
            "message": "Login Successful",
            "user_id": user.id,
            "role": user.role,
            "access_token": token,
            "token_type": "bearer",
        }