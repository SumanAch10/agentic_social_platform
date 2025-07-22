# This is the database connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models import models

DATABASE_URL = "postgresql://postgres:1415@localhost:5432/Agentic_social_platform"

# Create Engine
engine = create_engine(DATABASE_URL)

#Create a session factory
SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine) 

Base = declarative_base()

