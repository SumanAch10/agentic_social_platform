# Business logic related to post
from fastapi import HTTPException,status,Depends,Cookie
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import UserPost
from app.schemas.users import UserPosts as pydantic_UserPost
from app.db.db import SessionLocal
from datetime import datetime
from app.utils.post_utils import get_current_user

# Function to create the posts
def create_post(post:pydantic_UserPost,jwt_refresh_token:str = Cookie(None)):
    db:Session = SessionLocal()
    # So i need to get the current user
    print(jwt_refresh_token)
    get_current_user(jwt_refresh_token)
