from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from database import Base

class Notification(Base):
    __tablename__ = "notification"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    screenshot_id = Column(String(36), ForeignKey("screenshot.id"), nullable=False, index=True)
    notification_time = Column(DateTime, nullable=False)  # 알림을 보낼 시간
    is_sent = Column(Boolean, default=False)  # 알림 전송 여부
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # 관계 설정
    user = relationship("User", back_populates="notifications")
    screenshot = relationship("Screenshot", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, screenshot_id={self.screenshot_id}, notification_time={self.notification_time}, is_sent={self.is_sent})>"