from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from user.infra.db_models.user import User

class Category(Base):
    __tablename__ = "category"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    screenshot = relationship("Screenshot", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
    

class Screenshot(Base):
    __tablename__ = "screenshot"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(2084), nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    price = Column(Integer, nullable=True)
    code = Column(Text, nullable=True)
    category_id = Column(String(36), ForeignKey(Category.id), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="screenshot")
    notifications = relationship("Notification", back_populates="screenshot", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Screenshot(id={self.id}, title={self.title}, description={self.description})>"
