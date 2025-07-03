from app.schemas import users
from sqlalchemy.orm import Session
from fastapi import FastAPI,HTTPException,status,APIRouter,Depends
from app.db import db
from app.schemas.users import UserCreate,UserLogin
from app.models import models
from app.services import services


router = APIRouter()
# print(type(router))

@router.post("/user_create")
def create_user_route(user: UserCreate):
    return services.create_user(user)

# Loggin in an user
@router.post("/user_login")
def login_user(user:UserLogin):
    return services.login_user(user)

            
    
        
        

