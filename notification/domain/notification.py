from datetime import datetime
from dataclasses import dataclass
from screenshot.domain.screenshot import Screenshot

@dataclass
class Notification:
    id: str
    user_id: str
    screenshot_id: str
    notification_time: datetime
    time_description: str
    message: str
    is_sent: bool
    created_at: datetime
    updated_at: datetime

    user: "User" = None
    screenshot: "Screenshot" = None