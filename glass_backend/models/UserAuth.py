from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str

class RecentActivityCreate(BaseModel):
    action: str
    detail: str

class RecentActivityResponse(BaseModel):
    id: int
    user_email: str
    action: str
    detail: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)