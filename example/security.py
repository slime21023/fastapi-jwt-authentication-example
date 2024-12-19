import os
from datetime import timedelta
from fastapi_jwt import JwtAccessBearer
from passlib.context import CryptContext
from jose import jwt

AUTH_SECRET = os.getenv("AUTH_SECRET", "secret")
VERIFY_SECRET = os.getenv("VERIFY_SECRET", "verify_secret")
crypt_ctx = CryptContext(schemes=["argon2"])

access_security = JwtAccessBearer(
    secret_key=AUTH_SECRET,
    algorithm="HS256",
    access_expires_delta=timedelta(hours=4),
    refresh_expires_delta=timedelta(hours=18),
)


def hash_password(password: str) -> str:
    return crypt_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_ctx.verify(password, hashed_password)


def create_verify_token(data: dict) -> str:
    return jwt.encode(data, VERIFY_SECRET, algorithm="HS256")

def decode_verify_token(token: str) -> dict:
    return jwt.decode(token, VERIFY_SECRET, algorithms=["HS256"])