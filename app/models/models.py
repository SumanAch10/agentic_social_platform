
from sqlalchemy import Column,Integer, String
from app.db.db import Base
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
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, user_name='{self.user_name}', email='{self.email}')>"









