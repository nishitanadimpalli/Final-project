from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


# -----------------------------
# Password Hashing Config
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "mysecretkey123"   # ❗ you can later move this to .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -----------------------------
# Password Hashing
# -----------------------------
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# JWT Token Creation
# -----------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT containing the user's email as 'sub'.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# -----------------------------
# Decode Token + Get Current User
# -----------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Read JWT token → validate → decode → return User from DB.
    Used in all protected routes like /calculations.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        # Token invalid or expired
        raise credentials_exception

    # Check if user exists in DB
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user
