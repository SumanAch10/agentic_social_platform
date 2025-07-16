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
def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str)->bool:
    return pwd_context.verify(plain_password,hash_password)

# Creating the access token
def create_access_token(token_payload : dict):
    expiry_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    # Adding the expiry_time to the payload
    token_payload.update({"exp":expiry_time})
    jwt_token = jwt.encode(claims = token_payload,key = SECRET_KEY,algorithm = ALGORITHM)
    return jwt_token

# Creating the refresh token
def create_refresh_token(token_payload : dict):
    pass

# Verigying the token and then creating a db session
def verify_access_token(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials"
    )
    try:        
        # Now i got the token, it's time to decode it 
        payload = jwt.decode(token,key=SECRET_KEY, algorithms=[ALGORITHM])
        # Getting the user email
        user_email = payload.get("sub")
        
        if not user_email:
            raise credentials_exception
        
        return user_email
    
    except JWTError:
        raise credentials_exception


