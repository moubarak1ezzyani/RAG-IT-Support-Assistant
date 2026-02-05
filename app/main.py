# Point d'entrée de l'application (lancement FastAPI)
from fastapi import FastAPI, Depends
from .db.database import engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from .db.database import Base, SessionLocal
from typing import Annotated

app=FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy=Annotated[Session, Depends(get_db)]

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
    