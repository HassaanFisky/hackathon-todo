import os
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()

def decode_jwt(token: str) -> dict:
    try:
        # Better Auth generates tokens. We assume it might use HS256 and the secret if we decode directly.
        # Alternatively, Better Auth manages sessions, but you can decode JWT if you use the jwt session plugin.
        # Let's decode relying on python-jose without strict audience validation for the hackathon.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    token = credentials.credentials
    payload = decode_jwt(token)
    
    # Better Auth token payload usually contains the user id (often named `id` or `sub`)
    # Depends on better-auth configuration. Usually `id` or `sub`.
    user_id = payload.get("id") or payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return user_id
