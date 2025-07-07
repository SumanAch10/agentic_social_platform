from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import User  # SQLAlchemy model
from app.schemas.users import UserCreate,UserLogin # Pydantic model
from app.db.db import SessionLocal
from app.utils.utils import hash_password,verify_password,create_access_token

def create_user(user:UserCreate):
    # Creating the session(a temporary workspace)
    db:Session = SessionLocal()
    print("Printing the session:,",db)
    try:
        existing_user = db.query(User).filter(( User.user_name == user.user_name ) | (User.email ==
        user.email)).first()
        print("Printing existing user: ", existing_user)
        # If there is existing user, don't let it enter the database
        if existing_user:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,detail = "User with this username or email already exists"
            )
        
        # Hashing the password before putting into database
        hashed_password = hash_password(user.password)
        print("after hashing the password")
    #    If no existing user
        new_user = User(user_name = user.user_name,password = hashed_password ,email = user.email)
    
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return{"message":f"User with {user.user_name} created succesfully"}
    
    finally:
        db.close()
          
def login_user(user:UserLogin):
    # Creating a db session
    db:Session = SessionLocal()
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
    
    # Verifying the email exists or not
        if not db_user:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    
    # Checking the password
        if not verify_password(plain_password=user.password,hash_password=db_user.password):
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    
    # token generation
    
        token_payload = {"sub":db_user.email}
        token = create_access_token(token_payload)
    
        return {
            "access_token":token,
            "token_type":"bearer"
        }
    finally:
        db.close()
        
def getUser(user_name:str):
    db:Session = SessionLocal()
    
    db_user = db.query(User).filter(User.user_name == user_name).first()
    
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "User not found")
    
    return db_user
    
    
    

    

