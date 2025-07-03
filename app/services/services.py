from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import User  # SQLAlchemy model
from app.schemas.users import UserCreate  # Pydantic model
from app.db import SessionLocal
from app.utils import hash_password

def create_user(user:UserCreate):
    db: Session = SessionLocal()
    
    try:
        # 1. Check for existing user
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.user_name == user.user_name)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )

        # 2. Hash the password
        hashed_pwd = hash_password(user.password)

        # 3. Create the User SQLAlchemy object
        new_user = User(
            user_name=user.user_name,
            email=user.email,
            password=hashed_pwd
        )

        # 4. Add to session and commit
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 5. Return new user (or a success message)
        return {"message": "User created successfully", "user_id": new_user.id}

    finally:
        db.close()
    

    
    
    

    

