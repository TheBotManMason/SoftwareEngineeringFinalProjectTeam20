from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)  # Changed to nullable=False
    customer_address = Column(String(255))
    order_type = Column(String(20))
    status = Column(String(20), default="pending")
    total_amount = Column(Float, nullable=False, default=0.0)
    discount_applied = Column(Float, default=0.0)  # Make sure this exists
    promo_code = Column(String(50))
    tracking_number = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    reviews = relationship("Review", back_populates="order")