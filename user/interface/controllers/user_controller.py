from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from containers import Container
from user.application.user_service import UserService
from dependency_injector.wiring import Provide, inject
from common.auth import get_current_user, get_admin_user, CurrentUser


router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: str
    updated_at: str


class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


@router.post("", status_code=201)
@inject
def create_user(user: CreateUserBody,
                user_service: UserService = Depends(Provide[Container.user_service])
) -> UserResponse:
    created_user = user_service.create_user(user.name, user.email, user.password)
    return created_user


@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    updated_user = user_service.update_user(
        user_id=current_user.id, 
        name=body.name, 
        password=body.password)
    return updated_user

@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_admin_user),
    user_service: UserService = Depends(Provide[Container.user_service])
) -> GetUsersResponse:
    total_count, users = user_service.get_users(page, items_per_page)
    return {"total_count": total_count, "page": page, "users": users}


@router.delete("", status_code=204)
@inject
def delete_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user_service.delete_user(current_user.id)
    return None


@router.post("/login")
@inject
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    access_token = user_service.login(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}