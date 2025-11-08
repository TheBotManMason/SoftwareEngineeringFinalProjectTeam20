from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, index=True, nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)

    menu_item = relationship("MenuItem", back_populates="order_items")
    orders = relationship("Order", back_populates="order_items")
