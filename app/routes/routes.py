from app.schemas import users
from fastapi import FastAPI,HTTPException,status,APIRouter
from app.db import db
from app.models import models

router = APIRouter()

# Signing a new user
@router.post("/user_create")
def create_user():
    pass

# Loggin in an user
@router.post("user_login")
def login_user():
    pass

            
    
        
        

