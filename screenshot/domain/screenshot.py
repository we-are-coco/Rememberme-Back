from dataclasses import dataclass
from datetime import datetime
from notification.domain.notification import Notification
from category.domain.category import Category


@dataclass
class Screenshot:
    id: str
    user_id: str
    title: str
    category_id: str
    description: str
    url: str
    start_date: datetime | None
    end_date: datetime | None
    price: float | None
    code: str | None
    created_at: datetime
    updated_at: datetime

    category: Category | None = None
    notifications: list["Notification"] | None = None