from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import orderitemscontroller
from ..schemas import order_items
from ..dependencies.database import get_db

router = APIRouter(tags=['OrderItems'], prefix="/order_items")  # Lowercase!

@router.post("/", response_model=order_items.OrderItem)
def create(request: order_items.OrderItemCreate, db: Session = Depends(get_db)):
    return orderitemscontroller.create(db=db, request=request)

@router.get("/", response_model=list[order_items.OrderItem])
def read_all(db: Session = Depends(get_db)):
    return orderitemscontroller.read_all(db)

@router.get("/{item_id}", response_model=order_items.OrderItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return orderitemscontroller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=order_items.OrderItem)
def update(item_id: int, request: order_items.OrderItemUpdate, db: Session = Depends(get_db)):
    return orderitemscontroller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return orderitemscontroller.delete(db=db, item_id=item_id)