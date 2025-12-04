from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_connector import get_db
from typing import List
from database.AdminTable import RecentActivity
from models.UserAuth import RecentActivityResponse
router = APIRouter(prefix="/admin",tags=["recent_activity"])


@router.get("/recent_activity", response_model=List[RecentActivityResponse])
def get_recent_activities(
    db: Session = Depends(get_db),
    limit: int = 20
):
    activities = (
        db.query(RecentActivity)
        .order_by(RecentActivity.created_at.desc())
        .limit(limit)
        .all()
    )
    return activities