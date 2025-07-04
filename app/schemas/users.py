# Defining the schemas for my users in this file
from pydantic import BaseModel,EmailStr,constr,root_validator

class UserCreate(BaseModel):
    user_name : str
    email:EmailStr
    password:constr(min_length=6)
    confirm_password:str
    
    @root_validator()
    def check_passwords_match(cls, values):
        pw = values.get("password")
        cpw = values.get("confirm_password")

        if pw != cpw:
            raise ValueError("Passwords do not match")

        return values
    
class UserLogin(BaseModel):
    email:EmailStr
    password:constr(min_length=6)

