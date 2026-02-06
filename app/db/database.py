# Connexion 
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Annotated
from fastapi import Depends
# var
load_dotenv()
DB_USER=os.getenv("db_user_env")
DB_PASSWORD=os.getenv("db_password_env")
DB_HOST=os.getenv("db_host_env")
DB_PORT=os.getenv("db_port_env","5432")
DB_NAME=os.getenv("db_name_env")

# link db : protocol://username:password@host:port/database_name
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine
engine = create_engine(db_url)

# session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base
Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy=Annotated[Session, Depends(get_db)]