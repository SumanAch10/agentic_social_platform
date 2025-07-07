from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt, JWTError

# Configuration variable
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
