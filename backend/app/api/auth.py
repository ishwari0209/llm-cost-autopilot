
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])
password_hasher = PasswordHash.recommended()
bearer_scheme = HTTPBearer()


class SignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def create_access_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": str(user_id), "exp": expires},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


@router.post("/signup", status_code=201)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    email = str(req.email).lower()

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")

    user = User(
        name=req.name.strip(),
        email=email,
        password_hash=password_hasher.hash(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return {
        "message": "Account created successfully.",
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    email = str(req.email).lower()
    user = db.query(User).filter(User.email == email).first()

    if (
        not user
        or not user.password_hash
        or not password_hasher.verify(req.password, user.password_hash)
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(user.id)
    return {
        "message": "Login successful.",
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "access_token": token,
        "token_type": "bearer",
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        subject = payload.get("sub")
        if not subject:
            raise HTTPException(status_code=401, detail="Invalid access token.")
        user_id = int(subject)
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired access token.")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists.")

    return user