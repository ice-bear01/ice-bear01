from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database_connector import get_db
from database.EmailVerTable import EmailCode
from models.EmailModel import SendCodeRequest, VerifyCodeRequest
from EmailAuth import send_email
import random
import tools
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/send-code")
def send_code(data: SendCodeRequest, db: Session = Depends(get_db)):

    code = str(random.randint(100000, 999999))
    expires_at = datetime.now(tools.PH_TZ) + timedelta(minutes=5)

    email_code = db.query(EmailCode).filter(
        EmailCode.email == data.email,
    ).first()

    if email_code:
        email_code.code = code
        email_code.expires_at = expires_at
    else:
        email_code = EmailCode(email=data.email, code=code, expires_at=expires_at)
        db.add(email_code)

    db.commit()
    send_email(data.email, code, purpose=data.purpose)

    return {"message": f"Verification code sent to email"}

@router.post("/verify-code")
def verify_code(data: VerifyCodeRequest, db: Session = Depends(get_db)):

    email_code = db.query(EmailCode).filter(
        EmailCode.email == data.email,
    ).first()

    if not email_code or email_code.code != data.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    if email_code.is_expired():
        raise HTTPException(status_code=400, detail="Code expired")

    db.delete(email_code)
    db.commit()

    return {"message": "email verified successfully"}
