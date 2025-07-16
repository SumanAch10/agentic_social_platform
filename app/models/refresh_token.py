from sqlalchemy import Column,String,DateTime,Boolean
from datetime import datetime,timedelta
from uuid import uuid4
from app.db.db import Base

# Model for the refresh token
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    token_id = Column(String,primary_key = True,default = lambda:str(uuid4()))
    user_email = Column(String,nullable=False,unique=True)
    expires_at = Column(DateTime,default = lambda:datetime.utcnow()+timedelta(days=7))
    is_revoked = Column(Boolean, default = False)


    
    
