from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Boolean, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ =  "promotions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    discount_percent = Column(DECIMAL(5,2), nullable=False)
    expiration_date = Column(DATETIME, nullable=False)
    active = Column(Boolean, nullable=False)