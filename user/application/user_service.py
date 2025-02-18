from dependency_injector.wiring import inject
from user.domain.repository.user_repo import IUserRepository
from ulid import ULID
from datetime import datetime
from user.domain.user import User
from fastapi import HTTPException, status
from utils.crypto import Crypto
from common.auth import Role, create_access_token
import requests


class UserService:
    @inject
    def __init__(self, user_repo: IUserRepository):
        self.user_repo: IUserRepository = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str, memo: str | None = None, fcm_token: str | None = None) -> User:
        _user = self.user_repo.find_by_email(email)
        if _user:
            raise HTTPException(status_code=422, detail="User already exists")
        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password) if password else None,
            memo=memo,
            fcm_token=fcm_token,
            notifications=[],
            created_at=now,
            updated_at=now
        )
        self.user_repo.save(user)
        return user
    
    def update_user(self, user_id: str, name:str | None = None, password: str | None = None, fcm_token: str | None = None) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=422, detail="User not found")

        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        if fcm_token:
            user.fcm_token = fcm_token
        user.updated_at = datetime.now()

        self.user_repo.update(user)
        return user
    
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)
        return users
    
    def get_user(self, user_id: str) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=422, detail="User not found")
        return user
    
    def get_user_by_email(self, email: str) -> User:
        user = self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(status_code=422, detail="User not found")
        return user
    
    def delete_user(self, user_id: str):
        self.user_repo.delete(user_id)

    def login(self, email: str, password: str) -> User:
        user = self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(status_code=422, detail="User not found")

        if not self.crypto.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token(payload={"user_id": user.id}, role=Role.USER)
        return access_token
    
    def kakao_login(self, access_token: str) -> User:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
        if response.status_code != 200:
            print('response', response.json())
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        kakao_user = response.json()
        email = kakao_user.get("kakao_account", {}).get("email")
        name = kakao_user.get("kakao_account", {}).get("profile", {}).get("nickname")
        print('kakao user', kakao_user)

        user = self.user_repo.find_by_email(email)
        if not user:
            user = self.create_user(name, email, None)
        return create_access_token(payload={"user_id": user.id}, role=Role.USER)
