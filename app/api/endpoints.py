import time
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models, schemas
from app.core import security
# from app.core.config import settings
# from django.conf import settings
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/query/", response_model=schemas.QueryResponse)
def create_query(
    query: schemas.QueryCreate, 
    request: Request, # <--- NOTE: We need Request to access the app.state
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    # Access the RAG pipeline we stored in main.py
    rag_pipeline = getattr(request.app.state, "rag_pipeline", None)

    if rag_pipeline:
        try:
            result = rag_pipeline.invoke({"input": query.question})
            answer_text = result["answer"]
        except Exception as e:
            print(f"RAG Error: {e}")
            answer_text = "I encountered an error processing your request."
    else:
        answer_text = "The AI system is currently offline."

    end_time = time.time()
    latency = (end_time - start_time) * 1000

    db_query = models.Query(
        user_id=current_user.id,
        question=query.question,
        answer=answer_text,
        cluster_id=1,
        latency_ms=latency
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    return db_query