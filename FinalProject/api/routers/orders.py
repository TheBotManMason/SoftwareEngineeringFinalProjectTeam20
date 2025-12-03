from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import ordercontroller
from ..schemas import order
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=order.Order)
def create(request: order.OrderCreate, db: Session = Depends(get_db)):
    return ordercontroller.create(db=db, request=request)


@router.get("/", response_model=list[order.Order])
def read_all(db: Session = Depends(get_db)):
    return ordercontroller.read_all(db)


@router.get("/{item_id}", response_model=order.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return ordercontroller.read_one(db, item_id=item_id)


@router.get("/track/{tracking_number}", response_model=order.Order)
def track_order(tracking_number: str, db: Session = Depends(get_db)):
    return ordercontroller.get_by_tracking(db, tracking_number=tracking_number)


@router.put("/{item_id}", response_model=order.Order)
def update(item_id: int, request: order.OrderUpdate, db: Session = Depends(get_db)):
    return ordercontroller.update(db=db, item_id=item_id, request=request)


@router.put("/{item_id}/status", response_model=order.Order)
def update_status(item_id: int, status: str, db: Session = Depends(get_db)):
    return ordercontroller.update_status(db, item_id=item_id, status=status)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return ordercontroller.delete(db=db, item_id=item_id)