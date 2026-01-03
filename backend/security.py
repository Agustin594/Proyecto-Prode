from passlib.context import CryptContext
import hashlib
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha)

def verify_password(password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha, hashed_password)

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)