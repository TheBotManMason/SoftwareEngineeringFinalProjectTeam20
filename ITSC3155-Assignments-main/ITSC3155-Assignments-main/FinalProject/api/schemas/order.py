from datetime import datetime
from typing import List
from pydantic import BaseModel

class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str = None
    order_type: str

class OrderCreate(OrderBase):
    order_items: List[dict]
    promo_code: str = None

class OrderUpdate(BaseModel):
    status: str = None

class Order(OrderBase):
    id: int
    tracking_number: str
    status: str
    total_amount: float
    discount_applied: float
    promo_code: str = None
    created_at: datetime

    class Config:
        from_attributes = True