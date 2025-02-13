from database import SessionLocal
from user.infra.db_models.user import User
from screenshot.infra.db_models.screenshot import Category, Screenshot
from datetime import datetime
from utils.crypto import Crypto


def create_test_user():
    with SessionLocal() as db:
        for i in range(50):
            user = User(
                id=f"UserID-{str(i).zfill(2)}",
                name=f"Testuser{i}",
                email=f"test-user{i}@test.com",
                password=Crypto().encrypt("password"),
                memo=None,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(user)
        user = User(
            id="UserID-50",
            name="mingi",
            email="pangshe10@gmail.com",
            password=Crypto().encrypt("test-password"),
            memo=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(user)
        db.commit()


def create_test_category():
    with SessionLocal() as db:
        for i,v in enumerate(['상품권', '쿠폰', '승차권', '기타']):
            category = Category(
                id=f"CategoryID-1{str(i)}",
                name=v,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(category)
        db.commit()


def create_test_screenshot():
    with SessionLocal() as db:
        for i in range(50):
            screenshot = Screenshot(
                id=f"ScreenshotID-{str(i).zfill(2)}",
                user_id=f"UserID-{str(i).zfill(2)}",
                title=f"TestScreenshot{i}",
                category_id=f"CategoryID-0{i % 4}",
                description=f"Description{i}",
                url=f"https://example.com/screenshot/{i}",
                start_date=datetime.now(),
                end_date=datetime.now(),
                price=1000.0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(screenshot)
        db.commit()