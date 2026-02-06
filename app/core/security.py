# Logique de hashage MDP et génération JWT
from fastapi import FastAPI, Depends, HTTPException, status
from app.db import User, Query,get_db
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


# --- var :
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY_env")
ALGO=os.getenv("ALGO_env")

# --- SECURITY ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")       # bcrypt : ALGO | deprecier les algo obsolète
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):    # dict : infos à mettre dans JWT
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)     # expiration : temps actuel + duree determinee
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get("sub")      # {"sub" : username}
        if username is None: raise HTTPException(status_code=401)       # 401 : Unauthorized
    except JWTError: raise HTTPException(status_code=401)
    user = db.query(User).filter(User.username == username).first()     # q : choix de table | f : condition | f : 1er resultat
    if user is None: raise HTTPException(status_code=401)
    return user
    