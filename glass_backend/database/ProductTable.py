from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Enum,Boolean
from sqlalchemy.orm import relationship
from database_connector import Base
from datetime import datetime
import enum
import tools
# -------------------------
# Product and related tables
# -------------------------
class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    product_image = Column(String, nullable=True)
    product_name = Column(String, nullable=False)
    product_price = Column(DECIMAL(10, 2), nullable=False)
    product_description = Column(String, nullable=False)
    is_archived = Column(Boolean,default=False)
    
    # Relationships
    benefits = relationship(
        "ProductBenefits", 
        back_populates="product", 
        cascade="all, delete-orphan"
    )
    specification = relationship(
        "ProductSpecifications", 
        back_populates="product", 
        cascade="all, delete-orphan"
    )
    installation_gallery = relationship(
        "InstallationGallery", 
        back_populates="product", 
        cascade="all, delete-orphan"
    )

class InstallationGallery(Base):
    __tablename__ = "installation_gallery"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    image = Column(String, nullable=True)
    description = Column(String, nullable=False)

    product = relationship("Product", back_populates="installation_gallery")


class ProductBenefits(Base):
    __tablename__ = "product_benefits"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    benefit_title = Column(String, nullable=False)
    benefit_description = Column(String, nullable=False)
    
    product = relationship("Product", back_populates="benefits")


class ProductSpecifications(Base):
    __tablename__ = "product_specification"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    specification_title = Column(String, nullable=False)
    specification_description = Column(String, nullable=False)
    
    product = relationship("Product", back_populates="specification")


# -------------------------
# Orders and related tables
# -------------------------
class OrderStatus(enum.Enum):
    Pending = "pending"
    Processing = "processing"
    Installed = "installed/shipped"
    Reject = "rejected"


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False) 
    created_at = Column(DateTime, default=lambda:datetime.now(tools.PH_TZ))
    status = Column(Enum(OrderStatus), default=OrderStatus.Pending) 
    order_note = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=False)
    barangay = Column(String, nullable=True)
    city = Column(String, nullable=False)
    province = Column(String, nullable=True)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer,nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    # Snapshot of product details
    product_category = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    product_image = Column(String, nullable=True)
    product_name = Column(String, nullable=False)
    product_price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Orders", back_populates="items")

# -------------------------
# Single Order Log Table
# -------------------------
class OrderLog(Base):
    __tablename__ = "order_log"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)  # original order id
    user_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tools.PH_TZ))
    status = Column(Enum(OrderStatus), nullable=False)
    order_note = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=False)
    barangay = Column(String, nullable=True)
    city = Column(String, nullable=False)
    province = Column(String, nullable=True)
    reject_reason = Column(String, nullable=True)
    
    # Snapshot of the product in this order
    product_id = Column(Integer, nullable=False)
    product_category = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    product_image = Column(String, nullable=True)
    product_name = Column(String, nullable=False)
    product_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
class DashboardData(Base):
    __tablename__ = "dashboard_data"

    id = Column(Integer, primary_key=True, index=True)
    product_category = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_quantity = Column(Integer, nullable=False, default=1)
    product_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime(timezone=True), default=lambda: datetime.now(tools.PH_TZ), nullable=False)
