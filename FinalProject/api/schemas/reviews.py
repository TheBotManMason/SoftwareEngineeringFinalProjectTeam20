from datetime import datetime
from pydantic import BaseModel

class ReviewBase(BaseModel):
    customer_name: str
    rating: int
    comment: str = None

class ReviewCreate(ReviewBase):
    order_id: int
    menu_item_id: int

class ReviewUpdate(BaseModel):
    rating: int = None
    comment: str = None

class Review(ReviewBase):
    id: int
    order_id: int
    menu_item_id: int
    created_at: datetime

    class Config:
        from_attributes = True