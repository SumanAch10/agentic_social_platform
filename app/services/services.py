from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import User  # SQLAlchemy model
from app.schemas.users import UserCreate  # Pydantic model
from app.db import SessionLocal
from app.utils import hash_password

def create_user(user:UserCreate):
    db:Session = SessionLocal()
    
    pass
    
    
    

    

