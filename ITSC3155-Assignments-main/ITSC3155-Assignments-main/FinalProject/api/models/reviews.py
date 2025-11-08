from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ =  "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(100), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    rating = Column(DECIMAL(2,1))
    comment = Column(String(500))
    created_at = Column(DATETIME, nullable=False, default=str(datetime.now()))
    
    customer = relationship("Customer", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="order_items")