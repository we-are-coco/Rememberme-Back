from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


screenshot_category = Table(
    "Screenshot_Category",
    Base.metadata,
    Column("screenshot_id", String(36), ForeignKey("Screenshot.id")),
    Column("category_id", String(36), ForeignKey("Category.id"))
)

class Screenshot(Base):
    __tablename__ = "Screenshot"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("User.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(2084), nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    price = Column(Integer, nullable=True)
    categories = relationship("Category", secondary=screenshot_category, back_populates="screenshots")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Screenshot(id={self.id}, title={self.title}, description={self.description}, image={self.image})>"


class Category(Base):
    __tablename__ = "Category"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    screenshots = relationship("Screenshot", secondary=screenshot_category, back_populates="categories")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"