from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt, JWTError
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

# Configuration variable
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user_login")
print("O auth scheme type: ",type(oauth2_scheme))

# print(oauth2_scheme)
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str)->bool:
    return pwd_context.verify(plain_password,hash_password)

def create_access_token(token_payload:dict):
    expiry_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adding the expiry_time to the payload
    token_payload.update({"exp":expiry_time})
    jwt_token = jwt.encode(claims = token_payload,key = SECRET_KEY,algorithm = ALGORITHM)
    return jwt_token

# Verigying the token and then creating a db session
def verify_access_token():
    pass


