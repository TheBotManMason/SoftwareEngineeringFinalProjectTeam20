from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import ingredients
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    existing_ingredient = db.query(ingredients.Ingredient).filter(ingredients.Ingredient.name == request.name).first()
    if existing_ingredient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this name already exists!"
        )

    new_item = ingredients.Ingredient(
        name=request.name,
        unit=request.unit,
        current_stock=request.current_stock,
        min_stock=request.min_stock
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(ingredients.Ingredient).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(ingredients.Ingredient).filter(ingredients.Ingredient.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(ingredients.Ingredient).filter(ingredients.Ingredient.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        # Check if name is being updated and if it conflicts
        if request.name:
            existing_ingredient = db.query(ingredients.Ingredient).filter(
                ingredients.Ingredient.name == request.name,
                ingredients.Ingredient.id != item_id
            ).first()
            if existing_ingredient:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another ingredient with this name already exists!"
                )

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(ingredients.Ingredient).filter(ingredients.Ingredient.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)