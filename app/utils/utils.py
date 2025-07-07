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

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str)->bool:
    return pwd_context.verify(plain_password,hash_password)

def create_access_token(data:dict):
    to_encode = data.copy()
    print("To encode variable value: ",to_encode)
    print(type(to_encode))
    print("UTC now func: ",datetime.utcnow())
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    print("After updating the to_encode variable: ",to_encode)
    return jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token using the secret and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # 'sub' stores subject — in our case, email

        # If email doesn't exist in token, token is invalid
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return email  # You can return this to your route function

    except JWTError:
        # If token is tampered or expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

