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

@router.post("/login_user")
def signIn_user(user:users.signIn_user):
    print("Sign in hit!!")
    for u in db.signUp_user:
        print("Inside the loop")
        if(u["email"] == user.email and u["password"] == user.password):
            print("Entering into the if else")
            db.signIn_user.append(user.dict())
            return {"message":"User authenticated succesfully"}  
        
        else:
            return {"message":"Email or password is invalid!!!!"}
            
    print("Outside the loop!!")
        
        

