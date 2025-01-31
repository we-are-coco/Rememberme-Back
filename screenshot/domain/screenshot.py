from dataclasses import dataclass
from datetime import datetime


@dataclass
class Category:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Screenshot:
    id: str
    user_id: str
    title: str
    category_id: str
    description: str
    url: str
    start_date: datetime
    end_date: datetime
    price: float
    created_at: datetime
    updated_at: datetime