from fastapi import HTTPException, status,Cookie,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import User,RefreshToken # SQLAlchemy model
from app.schemas.users import UserCreate,UserLogin # Pydantic model
from app.db.db import SessionLocal
from datetime import datetime,timedelta
from app.utils.auth_utils import hash_password,verify_password,create_access_token,verify_access_token,create_refresh_token,verify_refresh_token

def create_user(user:UserCreate):
    # Creating the session(a temporary workspace)
    db:Session = SessionLocal()
    # print("Printing the session:,",db)
    try:
        existing_user = db.query(User).filter(( User.user_name == user.user_name ) | (User.email ==
        user.email)).first()
        # print("Printing existing user: ", existing_user)
        # If there is existing user, don't let it enter the database
        if existing_user:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,detail = "User with this username or email already exists"
            )
        
        # Hashing the password before putting into database
        hashed_password = hash_password(user.password)
        # print("after hashing the password")
    #    If no existing user
        new_user = User(user_name = user.user_name,password = hashed_password ,email = user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return{"message":f"User with {user.user_name} created succesfully"}
    
    finally:
        db.close()
        
# Login function that returns access token and refresh token
def login_user(user:UserLogin):
    # Creates a session
    db:Session = SessionLocal()
    print(db)
    try:
        # Checking if the email exist in my database
        find_user = db.query(User).filter(User.email == user.email).first()    
        if find_user is None:
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
            
            # It is creating an instance of JSONResponse 
            response = JSONResponse(content = {
                "access_token":jwt_access_token,
                "token_type":"bearer"
                })

            # Setting up httponly cookie for refresh token
            # Before returning the response, let's store the jwt_refresh_token in the db
            is_jwt_refresh = db.query(RefreshToken).filter((RefreshToken.user_id == find_user.id)).first()
    
            if is_jwt_refresh is None or is_jwt_refresh.expires_at < datetime.utcnow() :
                # It means either the token has expired or there doesn't exist a token
                # Give a new token to the user in this case
                jwt_refresh_token = create_refresh_token(current_user_email)
                jwt_expiry = datetime.utcnow()+timedelta(days = 7)
                refresh_token = RefreshToken(token = jwt_refresh_token,user_id = find_user.id,expires_at = jwt_expiry)
                response.set_cookie(
                key = "jwt_refresh_token",
                value = jwt_refresh_token,
                httponly = True,
                secure = True,
                samesite = "strict",
                )
                db.add(refresh_token)
                db.commit()
                db.refresh(refresh_token)
            
            response.set_cookie(
                key = "jwt_refresh_token",
                value = is_jwt_refresh.token,
                httponly = True,
                secure = True,
                samesite = "strict",
                )
            return response  
            # return {
            #     "key":"request done"
            # }   
        # If the (if condition is not evaluated then the password didn't matched)
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Password didn't match")      
    
    finally:
        db.close()    
        

# Function to renew the access token
def renew_access_token(jwt_refresh_token: str = Cookie(None)):
    # what if i don't recieve the jwt token
    if jwt_refresh_token is None:
        raise HTTPException(status_code = 401,detail = "Token doesn't Exist")
    
    user_email = verify_refresh_token(jwt_refresh_token)
    current_user_email = {"sub":user_email}
    jwt_access_token = create_access_token(current_user_email)

    response = JSONResponse(content = {
            "access_token":jwt_access_token,
            "token_type":"bearer"
            })
    return response
    
