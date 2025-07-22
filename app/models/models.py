
from sqlalchemy import Column,Integer, String, DateTime, Boolean,ForeignKey,func
from app.db.db import Base
from uuid import uuid4
from datetime import datetime,timedelta
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user_login'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # 🔗 ORM Relationship to RefreshToken
    refresh_tokens = relationship(
        "RefreshToken",
        back_populates = "user",
        cascade = "all, delete-orphan"
    )
    
    user_post = relationship("UserPost",back_populates = "user", cascade="all,delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, user_name='{self.user_name}', email='{self.email}')>"

# Model for the refresh token
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    # So user_id is the foreign key that refers to the user_login table
    user_id = Column(Integer, ForeignKey("user_login.id", ondelete="CASCADE"),unique = True)  
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")
    
# Models for the posts

class UserPost(Base):
    __tablename__ = "user_posts"
    
    id = Column(Integer,primary_key = True, index = True)
    # userpost should be linked with the user
    user_id = Column(Integer, ForeignKey("user_login.id",ondelete = "CASCADE"),unique = True)
    user_text = Column(String,nullable = True)
    image_url = Column(String,nullable = True)
    created_at = Column(DateTime(timezone = True),server_default = func.now())
    
    likes = Column(Integer, default = 0)
    comments = Column(Integer, default = 0)
    share = Column(Integer, default = 0)
    
    user = relationship("User",back_populates = "user_post")







