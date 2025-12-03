from datetime import datetime
from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: str = None
    address: str = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: str = None
    phone: str = None
    email: str = None
    address: str = None

class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True