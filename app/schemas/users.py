# Defining the schemas for my users in this file
from pydantic import BaseModel,EmailStr,constr,root_validator
from pydantic import BaseModel, EmailStr, field_validator, model_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    user_name: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
class UserLogin(BaseModel):
    email:EmailStr
    password:constr(min_length=6)

