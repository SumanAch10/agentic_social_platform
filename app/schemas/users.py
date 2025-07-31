# Defining the schemas for my users in this file
from pydantic import BaseModel, EmailStr, field_validator, model_validator,constr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    user_name: str

    @model_validator(mode = 'after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
class UserLogin(BaseModel):
    email:EmailStr
    password:constr(min_length=6)

# Pydantic models for the post
class UserPosts(BaseModel):
    user_text:Optional[str] = None
    image_url:Optional[str] = None
    
    @model_validator(mode = "after")
    def check_image_text(self):
        if self.user_text is None and self.image_url is None:
            raise ValueError("Either user_text or image should be provided")
        return self
        
class PostResponse(BaseModel):
    user_text:Optional[str] = None
    image_url:Optional[str] = None
    

