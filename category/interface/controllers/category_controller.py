from fastapi import APIRouter, Depends
from category.application.category_service import CategoryService
from category.domain.category import Category
from dependency_injector.wiring import inject, Provide
from containers import Container
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime


router = APIRouter(prefix="/categories")

class CreateCategoryBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)


class CategoryResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

class GetCategoriesResponse(BaseModel):
    total_count: int
    page: int
    users: list[CategoryResponse]

@router.post('')
@inject
def create_category(
        category: CreateCategoryBody,
        category_service: CategoryService = Depends(Provide[Container.category_service])
    ):
    return category_service.create_category(name=category.name)

@router.get('/{category_id}')
@inject
def get_category(category_id: str, category_service: CategoryService = Depends(Provide[Container.category_service])):
    return category_service.get_category(category_id)

@router.put('/{category_id}')
@inject
def update_category(category_id: str, category: dict, category_service: CategoryService = Depends(Provide[Container.category_service])):
    category['id'] = category_id
    return category_service.update_category(category)

@router.delete('/{category_id}')
@inject
def delete_category(category_id: str, category_service: CategoryService = Depends(Provide[Container.category_service])):
    return category_service.delete_category(category_id)

@router.get('')
@inject
def get_categories(
    page: int = 1,
    items_per_page: int = 10,
    category_service: CategoryService = Depends(Provide[Container.category_service])
):
    return category_service.get_categories(page, items_per_page)