# Business logic related to post
from fastapi import HTTPException,status,Depends
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import UserPost
from app.schemas.users import UserPosts
from app.db.db import SessionLocal
from datetime import datetime

# Function to create the post
# def create_post():
#     pass

