from pydantic import BaseModel, EmailStr

class SendCodeRequest(BaseModel):
    email: EmailStr
    purpose: str
    
class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str 
