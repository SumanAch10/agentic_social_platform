
from sqlalchemy import Column,Integer, String
from app.db import Base

class User(Base):
    __tablename__ = 'user_login'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_name = Column(String, unique = True,nullable = False)
    email = Column(String, unique = True ,nullable = False)
    password = Column(String,nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, user_name='{self.user_name}', email='{self.email}')>"








