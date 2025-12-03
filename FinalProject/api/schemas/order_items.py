from pydantic import BaseModel

class OrderItemBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: int = None
    price: float = None

class OrderItem(OrderItemBase):
    id: int

    class Config:
        from_attributes = True