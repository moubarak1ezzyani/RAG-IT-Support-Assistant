# Point d'entrée de l'application (lancement FastAPI)
from fastapi import FastAPI, Depends, HTTPException, status
from app.db.database import engine, Base, SessionLocal, get_db
from app.db.models import User, Query
from app.db.schemas import UserBase
from app.core.security import pwd_context, OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from app.core.security import create_access_token
from app.rag.vector_db import main 


app=FastAPI()
Base.metadata.create_all(bind=engine)
# routers
# app.include_router(auth.router)
# app.include_router(questions.router)


# --- Sign Up
@app.post("/register")      # path = "/register"
def register(user: UserBase, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():       # SELECT * FROM users WHERE username = usernameL LIMIT 1;
        raise HTTPException(status_code=400, detail="Username already registered")  # 400 : Bad Request
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user) 
    db.commit()     # <=> INSERT INTO
    return {"message": "User created"}

# --- login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/similarity")
def search_similarity():
    result=main()
