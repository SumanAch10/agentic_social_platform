# Defining the schemas for my users in this file
from pydantic import BaseModel,EmailStr

class signIn_user(BaseModel):
    email:EmailStr
    password:str
    
class signUp_user(BaseModel):
    email:EmailStr
    password:str
    confirm_password:str

