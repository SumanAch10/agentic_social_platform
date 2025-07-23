from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.db.db import SessionLocal

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 7

def get_current_user(jwt_refresh_token:str)-> str:
    print("Refresh_Token: ", jwt_refresh_token)