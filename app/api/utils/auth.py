from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.database import blacklist_collection
import os

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()

# 🔐 Create Access Token (short-lived)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = 15)
    to_encode.update({ "exp": expire , "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔐 Create Refresh Token (long-lived)
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days = 7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔐 Verify Access Token (used in protected routes)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        email = payload.get("sub")
        if not isinstance(email, str):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid token")
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def verify_refresh_token(refresh_token: str):
    try:
        blacklisted = blacklist_collection.find_one({"token": refresh_token})
        if blacklisted:
            raise HTTPException(status_code=401, detail="Token blacklisted")
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        email = payload.get("sub")

        if not isinstance(email, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return email

    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")


