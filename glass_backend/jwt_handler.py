from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Cookie
from tools import PH_TZ  

JWT_SECRET = "my_key"  
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 120  

def create_jwt_token(email: str) -> str:
    expire = datetime.now(PH_TZ) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire.timestamp()}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(access_token: str = Cookie(None)) -> str:
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return verify_jwt_token(access_token)
