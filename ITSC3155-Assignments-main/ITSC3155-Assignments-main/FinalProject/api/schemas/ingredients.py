from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    unit: str
    current_stock: float
    min_stock: float

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: str = None
    unit: str = None
    current_stock: float = None
    min_stock: float = None

class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True