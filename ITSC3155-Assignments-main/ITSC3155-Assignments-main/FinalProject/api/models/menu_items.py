from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Boolean, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ =  "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(DECIMAL(10,2), nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    order_items = relationship("OrderItem", back_populates="menuitem")
    reviews = relationship("Review", back_populates="menuitem")