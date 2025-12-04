from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional

class AddOrder(BaseModel):
    product_id: int
    quantity: int
    order_note: Optional[str] = None

class DeliveryAddress(BaseModel):
    house_number: Optional[str]
    street: str
    barangay: Optional[str]
    city: str
    province: Optional[str]

class OrderResponse(BaseModel):
    order_id:int
    quantity:int
    product_image:str
    product_category:str
    product_type:str
    product_name:str
    product_price:float
    total_price:float
    status:str
    created_at:datetime
    order_note: Optional[str] = None
    delivery_address: Optional[DeliveryAddress] = None

    model_config = ConfigDict(from_attributes=True)


class AdminOrderUpdate(BaseModel):
    status:str

class OrderResponseAdmin(OrderResponse):
    user_email:str
    product_id:int


class DashboardDataResponse(BaseModel):
    id: int
    product_category: str
    product_name: str
    product_quantity: int
    product_price: float
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)

class PendingOrdersCountResponse(BaseModel):
    pending_count: int

    model_config = ConfigDict(from_attributes=True)


class OrderLogResponse(BaseModel):
    id: int
    order_id: int
    user_email: str
    created_at: datetime
    status: str
    delivery_address: DeliveryAddress
    reject_reason: Optional[str] = None
    product_id: int
    product_category: str
    product_type: str
    product_image: str
    product_name: str
    product_price: float
    quantity: int
    order_note: Optional[str] = None

class RejectOrderPayload(BaseModel):
    reason: str