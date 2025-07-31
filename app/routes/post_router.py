# this file will handle post routing part
from app.services import post_services
from app.utils import post_utils
from fastapi import APIRouter,Depends
from app.schemas.users import UserPosts as pydantic_Userposts


router = APIRouter(prefix = "/posts")
# ,current_userId= Depends(post_utils.get_current_userId)

@router.post("/create_post")
def create_user_post(my_post:pydantic_Userposts,current_userId = Depends(post_utils.get_current_userId)):
    return post_services.create_post(my_post,current_userId)

@router.delete("/delete_post")
def delete_user_post(current_userId:str = Depends(post_utils.get_current_userId)):
    return post_services.delete_post(current_userId)

@router.get("/getposts")
def get_all_posts():
    return post_services.show_all_posts()