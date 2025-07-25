from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status,Cookie
from fastapi.security import OAuth2PasswordBearer
from app.db.db import SessionLocal
from app.models.models import User

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 7

# this function gives current user id
def get_current_userId(jwt_refresh_token:str = Cookie(None))-> str:
    db:Session = SessionLocal()
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,detail = "Invalid credentials")
    try:
        payload = jwt.decode(jwt_refresh_token,SECRET_KEY,algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        db_user = db.query(User).filter(User.email == user_email).first()
        return db_user.id
        
    finally:
        # Preventing any leaks in case of error
        db.close()
    