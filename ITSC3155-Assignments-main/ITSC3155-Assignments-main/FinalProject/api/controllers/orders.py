from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..models import menu_items as menu_model
from ..models import order_items as order_item_model
from ..controllers import promotions as promo_controller
import uuid
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    # Generate tracking number
    tracking_number = str(uuid.uuid4())[:8].upper()

    # Calculate total and validate menu items
    total_amount = 0
    order_items_data = []

    for item in request.order_items:
        menu_item = db.query(menu_model.MenuItem).filter(
            menu_model.MenuItem.id == item['menu_item_id'],
            menu_model.MenuItem.is_available == 1
        ).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Menu item {item['menu_item_id']} not found!")

        item_total = menu_item.price * item['quantity']
        total_amount += item_total
        order_items_data.append({
            'menu_item_id': item['menu_item_id'],
            'quantity': item['quantity'],
            'price': menu_item.price
        })

    # Apply promotion if valid
    final_amount = total_amount
    discount_applied = 0

    if request.promo_code:
        try:
            promotion = promo_controller.validate_promo(db, request.promo_code)
            discount_amount = total_amount * (promotion.discount_percent / 100)
            final_amount = total_amount - discount_amount
            discount_applied = discount_amount
        except HTTPException:
            # If promo is invalid, continue without discount
            pass

    new_order = model.Order(
        customer_name=request.customer_name,
        customer_phone=request.customer_phone,
        customer_address=request.customer_address,
        order_type=request.order_type,
        total_amount=final_amount,
        discount_applied=discount_applied,
        promo_code=request.promo_code,
        tracking_number=tracking_number
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Create order items
        for item_data in order_items_data:
            order_item = order_item_model.OrderItem(
                order_id=new_order.id,
                menu_item_id=item_data['menu_item_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def get_by_tracking(db: Session, tracking_number: str):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def update_status(db: Session, item_id: int, status: str):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"status": status}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)