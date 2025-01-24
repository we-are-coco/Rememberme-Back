from dataclasses import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from typing import Annotated
from common.auth import CurrentUser, get_current_user
from containers import Container
from screenshot.application.screenshot_service import ScreenshotService
from datetime import datetime

router = APIRouter(prefix="/screenshot")

class ScreenshotResponse(BaseModel):
    id: str
    user_id: str
    title: str
    category: str
    description: str
    url: str
    start_date: datetime
    end_date: datetime
    price: float
    created_at: datetime
    updated_at: datetime


class CreateScreenshotBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    url: str = Field(min_length=1)
    start_date: datetime | None = Field(default=None)
    end_date: datetime | None = Field(default=None)
    price: float | None = Field(default=None)


@router.post("", status_code=201, response_model=ScreenshotResponse)
@inject
def create_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: CreateScreenshotBody,
        screenshot_service=Provide[Container.screenshot_service]
) -> ScreenshotResponse:
    screenshot = screenshot_service.create_screenshot(
        current_user.id,
        body.title,
        body.category,
        body.description,
        body.url,
        body.start_date,
        body.end_date,
        body.price
    )
    response = asdict(screenshot)
    return response


class GetScreenshotsResponse(BaseModel):
    total_count: int
    page: int
    screenshots: list[ScreenshotResponse]


@router.get("", response_model=GetScreenshotsResponse)
@inject
def get_screenshots(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        page: int = 1,
        items_per_page: int = 10,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> GetScreenshotsResponse:
    total_count, screenshots = screenshot_service.get_screenshots(
        current_user.id,
        page,
        items_per_page
    )
    response = GetScreenshotsResponse(
        total_count=total_count,
        page=page,
        screenshots=screenshots
    )
    return response


@router.get("/{screenshot_id}", response_model=ScreenshotResponse)
@inject
def get_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        screenshot_id: str,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> ScreenshotResponse:
    screenshot = screenshot_service.get_screenshot(current_user.id, screenshot_id)
    response = asdict(screenshot)
    return response


class UpdateScreenshotBody(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=64)
    description: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None)
    url: str | None = Field(default=None, min_length=1)


@router.put("/{screenshot_id}", response_model=ScreenshotResponse)
@inject
def update_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        screenshot_id: str,
        body: UpdateScreenshotBody,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> ScreenshotResponse:
    screenshot = screenshot_service.update_screenshot(
        current_user.id,
        screenshot_id,
        body.url,
        body.title,
        body.description,
        body.category
    )
    response = asdict(screenshot)
    return response


@router.delete("/{screenshot_id}", status_code=204)
@inject
def delete_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        screenshot_id: str,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
):
    screenshot_service.delete_screenshot(current_user.id, screenshot_id)


@router.get("/category/{category}/screenshots", response_model=GetScreenshotsResponse)
@inject
def get_screenshot_by_category(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        category: str,
        page: int = 1,
        items_per_page: int = 10,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> GetScreenshotsResponse:
    total_count, screenshots = screenshot_service.get_screenshot_by_category(
        current_user.id,
        category,
        page,
        items_per_page
    )
    response = GetScreenshotsResponse(
        total_count=total_count,
        page=page,
        screenshots=[asdict(screenshot) for screenshot in screenshots]
    )
    return response