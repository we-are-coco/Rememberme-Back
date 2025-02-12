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
    brand: str | None
    type: str | None
    url: str
    date: str | None
    time: str | None
    from_location: str | None
    to_location: str | None
    location: str | None
    details: str | None
    start_date: datetime | None
    end_date: datetime | None
    price: float | None
    code: str | None
    created_at: datetime
    updated_at: datetime

    category: Category | None = None
    notifications: list["Notification"] | None = None