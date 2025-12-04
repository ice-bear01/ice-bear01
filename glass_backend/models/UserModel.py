from pydantic import BaseModel, EmailStr
from datetime import datetime
class UploadProfileImage(BaseModel):
    profile_image:str

class Address(BaseModel):
    house_number: str
    street: str
    barangay:str
    city:str
    province:str

class AddressResponse(Address):
    id:int
    is_active:bool
    class Config:
        from_attributes = True
class ActivateAddress(BaseModel):
    is_active: bool

class UserProfile(BaseModel):
    email: EmailStr
    profile_picture: str


class AdminProfile(BaseModel):
    email: str


class FeedbackCreate(BaseModel):
    rating: float
    comment: str

class FeedbackResponse(BaseModel):
    id: int
    user_email: str
    profile_image: str | None
    rating: float
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True