from dataclasses import dataclass
from datetime import datetime


@dataclass
class Category:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

    screenshot: list['Screenshot']
