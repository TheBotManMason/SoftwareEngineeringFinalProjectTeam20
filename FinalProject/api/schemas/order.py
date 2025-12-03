from datetime import datetime
from typing import List
from pydantic import BaseModel


class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str = None
    order_type: str
    customer_id: int = None

class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(OrderBase):
    order_items: List[OrderItemRequest]
    promo_code: str = None

class OrderUpdate(BaseModel):
    status: str = None

class Order(OrderBase):
    id: int
    customer_id: int
    tracking_number: str
    status: str
    total_amount: float
    discount_applied: float
    promo_code: str = None
    created_at: datetime
    customer_address: str = None


    class Config:
        from_attributes = True