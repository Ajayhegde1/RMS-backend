# app/middleware/jwt_middleware.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from typing import Optional
from ..utils.jwt import verify_access_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            if verify_access_token(token) is None:
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
        else:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return credentials.credentials

