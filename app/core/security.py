import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def hash_password(plain: str) -> str:
    """return bcrypt hash of a plaintext password"""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    """check a plaintext password against a stored hash"""
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()                              # don’t mutate caller’s dict
    expire = datetime.utcnow() + (
        expires_delta if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})                    # add expiration claim
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """decode a JWT, raise JWTError on failure"""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])