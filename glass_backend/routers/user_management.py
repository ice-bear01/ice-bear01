from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_connector import get_db
from database.UsersAccountTable import User

router = APIRouter(prefix="/admin/users", tags=["admin-users"])

# ---------------- Get All Users ----------------
@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "user_id": u.user_id,
            "email": u.email,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]

# ---------------- Update User Status ----------------
@router.put("/{user_id}/status")
def update_user_status(user_id: int, is_active: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = is_active
    db.commit()
    db.refresh(user)

    return {"message": "User status updated", "is_active": is_active}
