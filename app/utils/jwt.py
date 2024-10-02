# app/utils/jwt.py
import jwt
from datetime import datetime, timedelta
from ..config import JWT_SECRET_KEY, JWT_EXPIRATION_MINUTES
# import logging

# logger = logging.getLogger(__name__)

# if JWT_SECRET_KEY is None:
#     raise ValueError("JWT_SECRET_KEY is not set")
# if JWT_EXPIRATION_MINUTES is None:
#     raise ValueError("JWT_EXPIRATION_MINUTES is not set")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
