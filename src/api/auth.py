"""
OAuth2 Authentication and JWT Token validation.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import hashlib
import hmac
import jwt

from .config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    exp: Optional[datetime] = None


class User(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
    is_active: bool = True


users_db = {
    "user1": {
        "user_id": "user1",
        "username": "admin",
        "email": "admin@shipsmart.com",
        "hashed_password": "hashed_password_here",
        "is_active": True,
    }
}


def hash_password(password: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire.isoformat()})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        exp = payload.get("exp")

        if user_id is None:
            return None

        return TokenData(user_id=user_id, exp=exp)
    except jwt.PyJWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    user_dict = users_db.get(token_data.user_id)
    if user_dict is None:
        raise credentials_exception

    return User(**user_dict)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token."""
    user = users_db.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        data={"sub": user["user_id"]},
        expires_delta=timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(username: str, password: str, email: str):
    """Register a new user."""
    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    user_id = f"user{len(users_db) + 1}"
    users_db[username] = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "hashed_password": hash_password(password),
        "is_active": True,
    }

    return {"user_id": user_id, "username": username}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info."""
    return current_user


@router.get("/verify")
async def verify_token_endpoint(token: str):
    """Verify a token."""
    token_data = verify_token(token)
    if token_data:
        return {"valid": True, "user_id": token_data.user_id}
    return {"valid": False}
