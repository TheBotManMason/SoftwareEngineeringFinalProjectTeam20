from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import ingredientcontroller
from ..schemas import ingredient
from ..dependencies.database import get_db

router = APIRouter(tags=['Ingredients'], prefix="/ingredients")

@router.post("/", response_model=ingredient.Ingredient)
def create(request: ingredient.IngredientCreate, db: Session = Depends(get_db)):
    return ingredientcontroller.create(db=db, request=request)

@router.get("/", response_model=list[ingredient.Ingredient])
def read_all(db: Session = Depends(get_db)):
    return ingredientcontroller.read_all(db)

@router.get("/{item_id}", response_model=ingredient.Ingredient)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return ingredientcontroller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=ingredient.Ingredient)
def update(item_id: int, request: ingredient.IngredientUpdate, db: Session = Depends(get_db)):
    return ingredientcontroller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return ingredientcontroller.delete(db=db, item_id=item_id)