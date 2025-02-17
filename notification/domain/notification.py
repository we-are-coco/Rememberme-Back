from datetime import datetime
from dataclasses import dataclass

@dataclass
class Notification:
    id: str
    user_id: str
    screenshot_id: str
    notification_time: datetime
    message: str
    is_sent: bool
    created_at: datetime
    updated_at: datetime

    user: "User" = None
    screenshot: "Screenshot" = None