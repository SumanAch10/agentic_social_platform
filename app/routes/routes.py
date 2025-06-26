from app.schemas import users
from fastapi import FastAPI,HTTPException,status,APIRouter
from app.db import db

router = APIRouter()

@router.post("/create_user")
def create_user(user:users.signUp_user):
    
    if(user.confirm_password == user.password):
        for u in db.signUp_user:
            if(u["email"] == user.email):
                raise HTTPException(status_code = 409,detail= "Email already registered")
        db.signUp_user.append(user.dict())
        return {"message":"User registered successfully","User":db.signUp_user}
    
    raise HTTPException(status_code = 400,detail="Password donot match")
        

