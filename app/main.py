# Point d'entrée de l'application (lancement FastAPI)
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from sqlalchemy.sql import func

# ==========================================
# 1. CONFIGURATION (Environment Variables)
# ==========================================
load_dotenv()

DB_USER = os.getenv("db_user_env", "postgres")
DB_PASSWORD = os.getenv("db_password_env", "password")
DB_HOST = os.getenv("db_host_env", "localhost")
DB_PORT = os.getenv("db_port_env", "5432")
DB_NAME = os.getenv("db_name_env", "postgres")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY_env", "supersecretkey") 
ALGORITHM = os.getenv("ALGO_env", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ==========================================
# 2. DATABASE SETUP
# ==========================================
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 3. MODELS (SQLAlchemy Tables)
# ==========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    queries = relationship("Query", back_populates="user")

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    cluster_id = Column(Integer, nullable=True)
    latency_ms = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="queries")

# ==========================================
# 4. SCHEMAS (Pydantic Models)
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class QueryBase(BaseModel):
    question: str

class QueryCreate(QueryBase):
    pass

class QueryResponse(QueryBase):
    id: int
    user_id: int
    answer: str
    cluster_id: Optional[int] = None
    latency_ms: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# 5. SECURITY UTILS
# ==========================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==========================================
# 6. AUTH DEPENDENCY
# ==========================================
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ==========================================
# 7. API APPLICATION
# ==========================================
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Note: OAuth2PasswordRequestForm expects "username" field, so we map email to it
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/query/", response_model=QueryResponse)
def create_query(query: QueryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fake_answer = f"Processed: {query.question}"
    
    db_query = Query(
        user_id=current_user.id,
        question=query.question,
        answer=fake_answer,
        cluster_id=1,
        latency_ms=120.5
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query
#-------------------------------------------
# from fastapi import FastAPI, Depends
# from .db.database import engine
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from .db.database import Base, SessionLocal
# from typing import Annotated

# app=FastAPI()
# Base.metadata.create_all(bind=engine)

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependancy=Annotated[Session, Depends(get_db)]

# # --- SECURITY ---
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")       # bcrypt : ALGO | deprecier les algo obsolète
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def create_access_token(data: dict):    # dict : infos à mettre dans JWT
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=30)     # expiration : temps actuel + duree determinee
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")      # {"sub" : username}
#         if username is None: raise HTTPException(status_code=401)       # 401 : Unauthorized
#     except JWTError: raise HTTPException(status_code=401)
#     user = db.query(User).filter(User.username == username).first()     # q : choix de table | f : condition | f : 1er resultat
#     if user is None: raise HTTPException(status_code=401)
#     return user
    
