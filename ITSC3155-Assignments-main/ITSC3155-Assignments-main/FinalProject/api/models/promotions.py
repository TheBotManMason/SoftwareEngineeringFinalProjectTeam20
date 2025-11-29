from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    discount_percent = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)