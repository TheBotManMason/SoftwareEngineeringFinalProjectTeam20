from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    description: str = None
    price: float
    calories: int = None
    category: str = None
    ingredients: str = None

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    calories: int = None
    category: str = None
    ingredients: str = None

class MenuItem(MenuItemBase):
    id: int
    is_available: int

    class Config:
        from_attributes = True