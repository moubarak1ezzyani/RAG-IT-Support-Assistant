# Modèles Pydantic (validation des données)
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# === USER SCHEMAS ===
# --- Base (Shared properties)
class UserBase(BaseModel):
    email: EmailStr
    password: str
# input : raw password
# class UserCreate(UserBase):
    

# response
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models


# === QUERY SCHEMAS ===
# Base (Shared properties)
class QueryBase(BaseModel):
    question: str

# input query
class QueryCreate(QueryBase):
    pass 

# Output (Response)
class QueryResponse(QueryBase):
    id: int
    user_id: int
    answer: str
    cluster_id: Optional[int] = None  # Optional : it might be null
    latency_ms: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# get User & Queries  : NESTED
class UserWithQueries(UserResponse):
    queries: List[QueryResponse] = []