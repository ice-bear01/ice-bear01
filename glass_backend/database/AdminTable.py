from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database_connector import Base
import tools

class RecentActivity(Base):
    __tablename__ = "recent_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    action = Column(String, nullable=False)
    detail = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),default=lambda: datetime.now(tools.PH_TZ))
  