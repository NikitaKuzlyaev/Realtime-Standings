from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "super-secret"  # при взломе поменять на "super-dupper-secret"
ALGORITHM = "HS256"


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int):
    return create_token({"sub": str(user_id)}, timedelta(hours=10))


def create_refresh_token(user_id: int):
    return create_token({"sub": str(user_id)}, timedelta(days=7))

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])