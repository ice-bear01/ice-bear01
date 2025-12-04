from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database_connector import Base
from datetime import datetime
import tools

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(tools.PH_TZ))

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    profile_image = relationship("ProfileImage", back_populates="user", uselist=False, cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=False)
    barangay = Column(String, nullable=True)
    city = Column(String, nullable=False)
    province = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)# here i added fpr activation ansd deactivation of acc


    user = relationship("User", back_populates="addresses")
    
class ProfileImage(Base):
    __tablename__ = "profile_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    image_url = Column(String, nullable=False)  

    user = relationship("User", back_populates="profile_image")



class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tools.PH_TZ))

    user = relationship("User", back_populates="feedbacks")
