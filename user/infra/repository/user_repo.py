from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO
from user.infra.db_models.user import User
from database import SessionLocal
from fastapi import HTTPException
from utils.db_utils import row_to_dict


class UserRepository(IUserRepository):
    def save(self, user: UserVO) -> None:
        new_user = User(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        with SessionLocal() as db:
            db.add(new_user)
            db.commit()
        
    def find_by_email(self, email) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return UserVO(**row_to_dict(user))

    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[UserVO]]:
        with SessionLocal() as db:
            query = db.query(User)
            total_count = query.count()
            offset = (page - 1) * items_per_page
            users = query.offset(offset).limit(items_per_page).all()

        return total_count, [UserVO(**row_to_dict(user)) for user in users]
    
    def update(self, user_vo: UserVO) -> None:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()

            if not user:
                raise HTTPException(status_code=422, detail="User not found")
            
            user.name = user_vo.name
            user.password = user_vo.password

            db.add(user)
            db.commit()
    
    def find_by_id(self, user_id):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return UserVO(**row_to_dict(user))
    
    def delete(self, user_id):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=422, detail="User not found")
            db.delete(user)
            db.commit()