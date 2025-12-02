from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import promotionscontroller
from ..schemas import promotions
from ..dependencies.database import get_db

router = APIRouter(tags=['Promotions'], prefix="/promotions")

@router.post("/", response_model=promotions.Promotion)
def create(request: promotions.PromotionCreate, db: Session = Depends(get_db)):
    return promotionscontroller.create(db=db, request=request)

@router.get("/", response_model=list[promotions.Promotion])
def read_all(db: Session = Depends(get_db)):
    return promotionscontroller.read_all(db)

@router.get("/{item_id}", response_model=promotions.Promotion)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return promotionscontroller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=promotions.Promotion)
def update(item_id: int, request: promotions.PromotionUpdate, db: Session = Depends(get_db)):
    return promotionscontroller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return promotionscontroller.delete(db=db, item_id=item_id)