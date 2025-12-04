from fastapi import APIRouter, Depends, HTTPException,Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func
from database_connector import get_db
from database.UsersAccountTable import User, ProfileImage, Admin, Feedback
from models.UserModel import UserProfile, UploadProfileImage, AdminProfile, FeedbackCreate, FeedbackResponse
from datetime import datetime
from typing import List
import tools

# ✅ Import your existing JWT helper
from jwt_handler import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# ---------------- User Profile ----------------
@router.get("/profile", response_model=UserProfile)
def get_user_profile(user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile_image_url = user.profile_image.image_url if user.profile_image else ""
    return UserProfile(email=user.email, profile_picture=profile_image_url)


# ---------------- Update Profile Image ----------------
@router.post("/upload-profile-image")
def update_profile_image(
    profile_data: UploadProfileImage,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_url = profile_data.profile_image

    if not user.profile_image:
        new_image = ProfileImage(user_id=user.user_id, image_url=image_url)
        db.add(new_image)
    else:
        user.profile_image.image_url = image_url

    db.commit()
    return {"message": "Profile image updated successfully", "image_url": image_url}


# ---------------- New Customer Count ----------------
@router.get("/new-customer-count")
def get_new_customer_count(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    count = db.query(User).filter(func.date(User.created_at) == today).count()
    return {"today_new_customers": count}


# ---------------- Admin Profile ----------------
@router.get("/admin/profile", response_model=AdminProfile)
def get_admin_profile(admin_email: str = Cookie(None), db: Session = Depends(get_db)):
    if not admin_email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    admin = db.query(Admin).filter(Admin.email == admin_email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    return AdminProfile(email=admin.email)


# ---------------- Add Feedback ----------------
@router.post("/feedback", response_model=FeedbackResponse)
def add_feedback(
    feedback_data: FeedbackCreate,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    feedback = Feedback(
        user_id=user.user_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment,
        created_at=datetime.now(tools.PH_TZ)
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    from database.AdminTable import RecentActivity
    recent_activity = RecentActivity(
        user_email=user_email,
        action="Feedback",
        detail="Added feedback",
        created_at=datetime.now(tools.PH_TZ)
    )
    db.add(recent_activity)
    db.commit()
    db.refresh(recent_activity)

    return FeedbackResponse(
        id=feedback.id,
        user_email=user.email,
        profile_image=user.profile_image.image_url if user.profile_image else None,
        rating=feedback.rating,
        comment=feedback.comment,
        created_at=feedback.created_at
    )


# ---------------- Fetch Feedbacks ----------------
@router.get("/feedbacks", response_model=List[FeedbackResponse])
def get_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).join(User).all()
    result = []
    for fb in feedbacks:
        result.append(
            FeedbackResponse(
                id=fb.id,
                user_email=fb.user.email,
                profile_image=fb.user.profile_image.image_url if fb.user.profile_image else None,
                rating=fb.rating,
                comment=fb.comment,
                created_at=fb.created_at
            )
        )
    return result
