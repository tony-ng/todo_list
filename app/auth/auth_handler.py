import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def sign_jwt(user_id: int):
    """Generate the JWT token"""
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str):
    """Decode the JWT and check if valid or not"""
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token["user_id"] if decoded_token["expires"] >= time.time() else None
    except:
        return {}
