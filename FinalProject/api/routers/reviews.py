from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import reviewscontroller
from ..schemas import reviews
from ..dependencies.database import get_db

router = APIRouter(tags=['Reviews'], prefix="/reviews")

@router.post("/", response_model=reviews.Review)
def create(request: reviews.ReviewCreate, db: Session = Depends(get_db)):
    return reviewscontroller.create(db=db, request=request)

@router.get("/", response_model=list[reviews.Review])
def read_all(
    menu_item_id: int = Query(None, description="Filter reviews by menu item ID"),
    db: Session = Depends(get_db)
):
    return reviewscontroller.read_all(db, menu_item_id=menu_item_id)

@router.get("/{item_id}", response_model=reviews.Review)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return reviewscontroller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=reviews.Review)
def update(item_id: int, request: reviews.ReviewUpdate, db: Session = Depends(get_db)):
    return reviewscontroller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return reviewscontroller.delete(db=db, item_id=item_id)