from sqlalchemy import Column, String, DateTime
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "category"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    screenshot = relationship("Screenshot", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"