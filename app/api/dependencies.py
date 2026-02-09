# Vérification token JWT, accès DB
from app.core.security import oauth2_scheme
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db
from app.db.models import User
from fastapi import Depends, HTTPException, status
from app.core.config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt



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