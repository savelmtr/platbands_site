import base64
import datetime
import time
from typing import Any

import general.settings as settings
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from .schemas import TokenSchema
from general.models import User
import xxhash


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def signJWT(user_id: str) -> TokenSchema:
    payload = {
        "user_id": user_id,
        "expires": time.time() + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

    return TokenSchema(access_token=token)


def decodeJWT(token: str) -> dict|None:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None


def generate_reset_password_hash(user: User, day: int):    
    hash = xxhash.xxh3_128_hexdigest(f'{user.id}{user.password}{user.last_login}{day}')
    day64 = base64.urlsafe_b64encode(str(day).encode()).decode()
    id64 = base64.urlsafe_b64encode(str(user.id).encode()).decode()
    return f'{id64}-{day64}-{hash}'
