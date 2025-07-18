from sqlalchemy import Column,String,DateTime,Boolean,Integer
from datetime import datetime,timedelta
from uuid import uuid4
from app.db.db import Base

# Model for the refresh token
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_login.id", ondelete="CASCADE"))  # ✅ fixed here
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")

    
    
