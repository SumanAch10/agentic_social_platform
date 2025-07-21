from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.db.db import SessionLocal

# Configuration variable
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user_login")
print("O auth scheme type: ",type(oauth2_scheme))

# Creating a db session
# def get_db():
#     db:Session = SessionLocal()
#     return db

# print(oauth2_scheme)
def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str)->bool:
    return pwd_context.verify(plain_password,hash_password)

# Creating the access token
def create_access_token(token_payload : dict):
    expiry_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    # Adding the expiry_time to the payload
    token_payload.update({"exp":expiry_time})
    jwt_access_token = jwt.encode(claims = token_payload,key = SECRET_KEY,algorithm = ALGORITHM)
    return jwt_access_token

# Creating the refresh token
def create_refresh_token(token_payload : dict):
    expiry_time = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token_payload.update({"exp":expiry_time})
    jwt_refresh_token = jwt.encode(claims = token_payload,key = SECRET_KEY,algorithm=ALGORITHM)
    return jwt_refresh_token

# Verifying the token and then creating a db session
def verify_access_token(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials"
    )
    try:        
        # Now i got the token, it's time to decode it 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise credentials_exception
        
        return user_email
    
    except JWTError:
        raise credentials_exception

def verify_refresh_token(jwt_refresh_token : str) ->str:
    # Writing my logic here, an verifing the refresh_token
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials"
    )
    try:
        payload = jwt.decode(jwt_refresh_token, key = SECRET_KEY,algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        
        if not user_email:
            raise credentials_exception
        
        is_expired = payload.get("exp")
        
        if is_expired < datetime.utcnow().timestamp():
            # It means the token has expired
            raise HTTPException(status_code = 401,detail = "Token has expired")
        # If the token hasn't expired
        return user_email
    
    except Exception:
        raise credentials_exception
