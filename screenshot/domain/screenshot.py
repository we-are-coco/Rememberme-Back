from dataclasses import dataclass
from datetime import datetime
from notification.domain.notification import Notification
from category.domain.category import Category


@dataclass
class Screenshot:
    id: str
    user_id: str | None
    title: str | None
    category_id: str | None
    description: str | None
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
    is_used: bool
    created_at: datetime
    updated_at: datetime

    category: Category | None = None
    notifications: list["Notification"] | None = None