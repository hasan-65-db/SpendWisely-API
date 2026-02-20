from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from oauth2 import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)