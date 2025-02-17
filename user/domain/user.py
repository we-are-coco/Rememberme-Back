from dataclasses import dataclass
from datetime import datetime
from notification.domain.notification import Notification


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str | None
    memo: str | None
    fcm_token: str | None
    notifications: list["Notification"] | None
    created_at: datetime
    updated_at: datetime

