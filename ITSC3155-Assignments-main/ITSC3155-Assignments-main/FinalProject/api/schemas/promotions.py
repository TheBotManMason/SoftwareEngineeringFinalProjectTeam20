from datetime import datetime
from pydantic import BaseModel

class PromotionBase(BaseModel):
    code: str
    description: str
    discount_percent: float

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    description: str = None
    is_active: bool = None

class Promotion(PromotionBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True