# this file will handle post routing part
from app.services import post_services
from fastapi import APIRouter,Depends
from app.schemas.users import UserPosts

router = APIRouter(prefix = "/posts")

@router.post("/create_post")
def create_user_post():
    pass
