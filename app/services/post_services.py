# Business logic related to post
from fastapi import HTTPException,status,Depends,Cookie
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import UserPost
from app.schemas.users import UserPosts as pydantic_UserPost
from app.db.db import SessionLocal
from datetime import datetime
from app.utils.post_utils import get_current_userId

# Function to create the posts
def create_post(post:pydantic_UserPost,current_userId):
    db: Session = SessionLocal()
    # Establishing the connection between posts and user table
    try:
        user_post = UserPost(user_text = post.user_text,user_id = current_userId,image_url = post.image_url)
        db.add(user_post)
        db.commit()
        db.refresh(user_post)
        
    finally:
        db.close()
