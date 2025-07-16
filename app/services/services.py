from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import User  # SQLAlchemy model
from app.models import refresh_token
from app.schemas.users import UserCreate,UserLogin # Pydantic model
from app.db.db import SessionLocal
from app.utils.utils import hash_password,verify_password,create_access_token,verify_access_token,create_refresh_token

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
    # Creates a session
    db:Session = SessionLocal()
    
    try:
        # Checking if the email exist in my database
        find_user = db.query(User).filter(User.email == user.email).first()    
        if not find_user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "User not found")
        
        # If the if condition isn't evaluated it means user exist, now i need to validate the password entered
        
        db_passoword = find_user.password
        is_passwoord_valid = verify_password(plain_password =user.password,hash_password = db_passoword)
        
        # If the password matched
        if is_passwoord_valid:
            # Authenticating the user and returning the jwt token as a response
            # Now generate the token in utils.py and return the token and token type as bearer
            current_user_email = {"sub":find_user.email}
            jwt_access_token = create_access_token(current_user_email)
            jwt_refresh_token = create_refresh_token(current_user_email)
            # print(current_user_email)
            return {"token":jwt_token,
                    "token_type":"bearer",
                    "User_email":f"{find_user.email}"
                    }
        
        # If the (if condition is not evaluated then the password didn't matched)
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Password didn't match")      
    
    finally:
        db.close()    
    
