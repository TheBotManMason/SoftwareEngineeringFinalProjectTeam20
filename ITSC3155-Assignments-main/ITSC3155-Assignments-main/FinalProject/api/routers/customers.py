from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import customercontroller
from ..schemas import customer
from ..dependencies.database import get_db

router = APIRouter(tags=['Customers'], prefix="/customers")

@router.post("/", response_model=customer.Customer)
def create(request: customer.CustomerCreate, db: Session = Depends(get_db)):
    return customercontroller.create(db=db, request=request)

@router.get("/", response_model=list[customer.Customer])
def read_all(db: Session = Depends(get_db)):
    return customercontroller.read_all(db)

@router.get("/{item_id}", response_model=customer.Customer)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return customercontroller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=customer.Customer)
def update(item_id: int, request: customer.CustomerUpdate, db: Session = Depends(get_db)):
    return customercontroller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return customercontroller.delete(db=db, item_id=item_id)