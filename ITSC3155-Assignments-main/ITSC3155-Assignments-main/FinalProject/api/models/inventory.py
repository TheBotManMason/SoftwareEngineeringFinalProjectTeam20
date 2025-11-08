from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Inventory(Base):
    __tablename__ =  "inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer)