from app.services import services
from fastapi import APIRouter,Depends
from app.schemas.users import UserCreate,UserLogin
from app.utils.utils  import verify_token

router = APIRouter()
# print(type(router))

@router.post("/user_create")
def create_user_route(user: UserCreate):
    return services.create_user(user)

# Loggin in an user
@router.post("/user_login")
def login_user(user:UserLogin):
    return services.login_user(user)

@router.get("/protected")
def get_protected_route(current_user_email: str = Depends(verify_token)):
    return {"message": f"Welcome {current_user_email}"}

@router.get("/{user_name}")
def get_byuser_name(user_name:str):
    return services.getUser(user_name)



            
    
        
        

