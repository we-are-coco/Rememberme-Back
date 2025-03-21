from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from category.infra.db_models.category import Category
    

class Screenshot(Base):
    __tablename__ = "screenshot"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    category_id = Column(String(36), ForeignKey(Category.id), nullable=True, index=True)
    description = Column(Text, nullable=True)
    brand = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    url = Column(String(2084), nullable=False)
    date = Column(String(255), nullable=True)
    time = Column(String(255), nullable=True)
    is_used = Column(Boolean, nullable=False, default=False)
    from_location = Column(String(255), nullable=True)
    to_location = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    price = Column(Integer, nullable=True)
    code = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="screenshot")
    notifications = relationship("Notification", back_populates="screenshot", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Screenshot(id={self.id}, title={self.title}, description={self.description[:10]}, notifications={self.notifications})>"
