from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders
from sqlalchemy.exc import SQLAlchemyError
import random
import string


def create(db: Session, request):
    from ..models.customers import Customer

    customer = db.query(Customer).filter(
        Customer.phone == request.customer_phone).first()
    if not customer:
        customer = Customer(
            name=request.customer_name,
            phone=request.customer_phone,
            email=None,
            address=request.customer_address
        )
        try:
            db.add(customer)
            db.commit()
            db.refresh(customer)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create customer: {error}"
            )
    total_amount = 0.0
    for item in request.order_items:
        from ..models.menu_items import MenuItem
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with id {item.menu_item_id} not found"
            )

        total_amount += menu_item.price * item.quantity
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    tracking_number = f"ORD{letters}{numbers}"

    new_item = orders.Order(
        customer_name=request.customer_name,
        customer_phone=request.customer_phone,
        customer_address=request.customer_address,
        order_type=request.order_type,
        customer_id=customer.id,  # Use the customer's ID (existing or newly created)
        total_amount=total_amount,
        tracking_number=tracking_number,
        promo_code=request.promo_code,
        status="pending"
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        from ..models.order_items import OrderItem
        for item in request.order_items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            order_item = OrderItem(
                order_id=new_item.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price=menu_item.price
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item


def read_all(db: Session):
    try:
        result = db.query(orders.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(orders.Order).filter(orders.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def get_by_tracking(db: Session, tracking_number: str):
    try:
        item = db.query(orders.Order).filter(orders.Order.tracking_number == tracking_number).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(orders.Order).filter(orders.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def update_status(db: Session, item_id, status: str):
    try:
        item = db.query(orders.Order).filter(orders.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"status": status}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        from ..models.order_items import OrderItem
        db.query(OrderItem).filter(OrderItem.order_id == item_id).delete(synchronize_session=False)

        item = db.query(orders.Order).filter(orders.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)