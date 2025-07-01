# Defining the schemas for my users in this file
from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    user_name : str
    email:EmailStr
    password:str
    confirm_password:str
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

