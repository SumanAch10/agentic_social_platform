from fastapi import HTTPException, status,Cookie,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import User,RefreshToken # SQLAlchemy model
from app.schemas.users import UserCreate,UserLogin # Pydantic model
from app.db.db import SessionLocal
from datetime import datetime,timedelta
from app.utils.utils import hash_password,verify_password,create_access_token,verify_access_token,create_refresh_token,get_db

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
            jwt_refresh_token = create_refresh_token(current_user_email)

            # It is creating an instance of JSONResponse 
            response = JSONResponse(content = {
                "access_token":jwt_access_token,
                "token_type":"bearer"
                })
            print("Inside the login fuction")
            # Setting up httponly cookie for refresh token
            response.set_cookie(
                key = "jwt_refresh_token",
                value = jwt_refresh_token,
                httponly = True,
                secure = True,
                samesite = "strict",
                    )
            # Before returning the response, let's store the jwt_refresh_token in the db
            jwt_expiry = datetime.utcnow()+timedelta(days = 7)
            refresh_token = RefreshToken(token = jwt_refresh_token,user_id = find_user.id,expires_at = jwt_expiry)
            db.add(refresh_token)
            db.commit()
            db.refresh(refresh_token)
            
            return response  
            # return {
            #     "key":"request done"
            # }   
        # If the (if condition is not evaluated then the password didn't matched)
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Password didn't match")      
    
    finally:
        db.close()    
        

def get_refresh_token(
    jwt_refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not jwt_refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(jwt_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 🔍 Get user from DB
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔒 Find matching refresh token in DB
    db_token = db.query(RefreshToken).filter(RefreshToken.token == jwt_refresh_token).first()
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token not recognized")

    # ⏳ Check expiration
    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # 🔑 Generate new access token
    new_access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
    
