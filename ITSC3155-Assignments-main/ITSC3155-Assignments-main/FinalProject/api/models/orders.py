from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(String(100), nullable=False)
    total_amount = Column(DECIMAL(10,2),nullable=False)
    status = Column(String(50), nullable=False)
    order_type = Column(String(50))
    created_at = Column(DATETIME, nullable=False, default=str(datetime.now()))

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="orders")