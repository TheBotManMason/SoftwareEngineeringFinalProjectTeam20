from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    customer_name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")