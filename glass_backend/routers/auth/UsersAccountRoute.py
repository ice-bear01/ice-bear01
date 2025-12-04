from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from database_connector import get_db
from models.UserAuth import UserCreate, UserLogin, AdminLogin
from database.UsersAccountTable import User, Admin
from pydantic import BaseModel
from datetime import datetime
from database.AdminTable import RecentActivity
import tools

from jwt_handler import create_jwt_token, get_current_user

router = APIRouter(prefix="/users/auth", tags=["users"])

# ---------------- Change Password ----------------
class ChangePasswordRequest(BaseModel):
    email: str
    new_password: str

@router.put("/change-password")
def change_password(request: ChangePasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = request.new_password
    db.commit()
    return {"message": "Password changed successfully"}


# ---------------- User Sign-Up ----------------
@router.post("/sign-up")
def sign_up_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email Already Exist")

    # Create new user
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token and set cookie
    token = create_jwt_token(new_user.email)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    # Log recent activity
    recent_activity = RecentActivity(
        user_email=new_user.email,
        action="Sign Up",
        detail="New account created",
        created_at=datetime.now(tools.PH_TZ)
    )
    db.add(recent_activity)
    db.commit()
    db.refresh(recent_activity)

    return {"message": "Account Created Successfully"}


# ---------------- User Login ----------------
@router.post("/login")
def login_user(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email,
        User.password == user.password
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Your account is banned. Contact admin.")

    # Generate JWT token and set cookie
    token = create_jwt_token(db_user.email)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {"message": "Logged in successfully"}


# ---------------- User Logout ----------------
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,  
        secure=False,   
        samesite="lax" 
    )
    return {"message": "Logged out successfully"}


# ---------------- Admin Login (optional cookie-based) ----------------
@router.post("/admin/login")
def admin_login(login_data: AdminLogin, response: Response, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == login_data.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    if admin.password != login_data.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    response.set_cookie(
        key="admin_email",
        value=admin.email,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": f"Welcome {admin.email}"}


# ---------------- Admin Logout ----------------
@router.post("/admin/logout")
def admin_logout(response: Response):
    response.delete_cookie(key="admin_email")
    return {"message": "Admin logged out successfully"}


# ---------------- Example Protected User Route ----------------
@router.get("/profile")
def profile(email: str = Depends(get_current_user)):
    return {"email": email}
