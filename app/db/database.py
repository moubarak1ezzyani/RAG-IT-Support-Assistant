# Connexion 
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# var
load_dotenv()
db_user=os.getenv("db_user_env")
db_password=os.getenv("db_password_env")
db_host=os.getenv("db_host_env")
db_port=os.getenv("db_port_env")
db_name=os.getenv("db_name_env")

# link db : protocol://username:password@host:port/database_name
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# engine
engine = create_engine(db_url)

# session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base
Base = declarative_base()


