# Tes routes (POST /query, POST /auth, etc.)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import models
from ..db import schemas
from ..db.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user_input: schemas.UserCreate, db: Session = Depends(get_db)):
    # schema -> models
    db_user = models.User(
        email=user_input.email, 
        hashed_password=user_input.password + "fakehash" 
    )
    
    # Save to db
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
