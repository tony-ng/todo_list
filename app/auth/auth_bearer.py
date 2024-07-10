from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """Check the HTTP request has valid JWT token or not"""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            user_id = self.verify_jwt(credentials.credentials)
            if not user_id:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return user_id
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str):
        try:
            user_id = decode_jwt(jwtoken)
        except:
            user_id = None

        return user_id
