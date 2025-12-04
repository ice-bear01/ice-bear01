from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database_connector import Base
import tools
class EmailCode(Base):
    __tablename__ = "email_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    def is_expired(self):
        return datetime.now(tools.PH_TZ) > self.expires_at
