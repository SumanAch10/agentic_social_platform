# this file will handle post routing part
from app.services import post_services
from fastapi import APIRouter,Depends
from app.schemas.users import UserPosts
# from 