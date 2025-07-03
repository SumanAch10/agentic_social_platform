# Defining the schemas for my users in this file
from pydantic import BaseModel,EmailStr,constr

class UserCreate(BaseModel):
    user_name : str
    email:EmailStr
    password:constr(min_length=6)
    confirm_password:str
    
class UserLogin(BaseModel):
    email:EmailStr
    password:constr(min_length=6)

