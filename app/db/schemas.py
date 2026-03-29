# Modèles Pydantic (validation des données)
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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