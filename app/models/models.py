from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer, String
from sqlalchem.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_login'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_name = Column(String, unique = True,nullable = False)
    email = Column(String, unique = True ,nullable = False)
    password = Column(String,nullable=False)
    
    def __repr__(self):
        pass

# Storing the database url and using it to connect with the database
DATABASE_URL = "postgresql://postgres:<your_password>@localhost:5432/Agentic_social_platform"

# Create Engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(DATABASE_URL)

print("Creating the session")
# Create a session
Session =  sessionmaker(bind = engine)
session = Session()



