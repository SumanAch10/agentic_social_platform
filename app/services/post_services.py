# Business logic related to post
from fastapi import HTTPException,status,Depends,Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import UserPost,User
from app.schemas.users import UserPosts as pydantic_UserPost
from app.db.db import SessionLocal
from datetime import datetime
from app.utils.post_utils import get_current_userId

# Function to create the posts
def create_post(post:pydantic_UserPost,current_userId):
    db: Session = SessionLocal()
    print(current_userId)
    user_name = db.query(User).filter((User.id == current_userId)).first().user_name
    try:
        user_post = UserPost(user_text = post.user_text,user_id = current_userId,image_url = post.image_url)
        db.add(user_post)
        db.commit()
        db.refresh(user_post)
        response = JSONResponse(content = {"User: ":f"{user_name} created a post"})
        return response
        
    finally:
        db.close()

#Function to delete the posts   
def delete_post(current_userId):
    db:Session = SessionLocal()
    try:
        user_posts = db.query(UserPost).filter(UserPost.user_id == current_userId).all()
        for post in user_posts:
            print({f"{post.id}":f"{post.user_text}"})
        user_input = int(input("Enter post_id to delete: "))           
        post_id_delete = next((p for p in user_posts if p.id == user_input),None)
        if not post_id_delete:
            raise HTTPException(status = status.HTTP_404_NOT_FOUND,detail = "Post not found")
        
        db.delete(post_id_delete)
        db.commit()
        print("Post deleted successfully")
        
    finally:
        db.close()
        
def show_all_posts():
    db:Session = SessionLocal()
    
    try:
        user_posts = db.query(UserPost).all()
        for post in user_posts:
            print(post.user_text)
        print(user_posts)
        print(type(user_posts))
    
    finally:
        db.close()
    
