from dataclasses import asdict
from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from typing import Annotated
from common.auth import CurrentUser, get_current_user
from containers import Container
from screenshot.application.screenshot_service import ScreenshotService
from datetime import datetime
import shutil

router = APIRouter(prefix="/screenshot")

class ScreenshotResponse(BaseModel):
    id: str
    user_id: str
    title: str
    category_id: str
    description: str
    brand: str | None
    type: str | None
    url: str
    date: str | None
    time: str | None
    from_location: str | None
    to_location: str | None
    location: str | None
    details: str | None
    start_date: datetime | None
    end_date: datetime | None
    price: float | None
    code: str | None
    created_at: datetime
    updated_at: datetime


class CreateScreenshotBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    category_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    url: str = Field(min_length=1)
    brand: str | None = Field(default=None)
    type: str | None = Field(default=None)
    date: str | None = Field(default=None)
    time: str | None = Field(default=None)
    from_location: str | None = Field(default=None)
    to_location: str | None = Field(default=None)
    location: str | None = Field(default=None)
    details: str | None = Field(default=None)
    start_date: datetime | None = Field(default=None)
    end_date: datetime | None = Field(default=None)
    price: float | None = Field(default=None)
    code: str | None = Field(default=None)



class UpdateScreenshotBody(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=64)
    category_id: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    brand: str | None = Field(default=None)
    type: str | None = Field(default=None)
    date: str | None = Field(default=None)
    time: str | None = Field(default=None)
    from_location: str | None = Field(default=None)
    to_location: str | None = Field(default=None)
    location: str | None = Field(default=None)
    details: str | None = Field(default=None)
    start_date: datetime | None = Field(default=None)
    end_date: datetime | None = Field(default=None)
    price: float | None = Field(default=None)
    code: str | None = Field(default=None)


@router.post("/upload")
@inject
def upload_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service]),
        file: UploadFile | None = None
):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = screenshot_service.upload_screenshot_image(current_user.id, file_path)
    return response


@router.post("", status_code=201, response_model=ScreenshotResponse)
@inject
def create_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: CreateScreenshotBody,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> ScreenshotResponse:
    screenshot = screenshot_service.create_screenshot(
        current_user.id,
        **body.model_dump()
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
        search_text: str = "",
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> GetScreenshotsResponse:
    total_count, screenshots = screenshot_service.get_screenshots(
        current_user.id,
        page,
        items_per_page,
        search_text,
    )
    screenshot_responses = [asdict(screenshot) for screenshot in screenshots]
    response = GetScreenshotsResponse(
        total_count=total_count,
        page=page,
        screenshots=screenshot_responses
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


@router.put("/{screenshot_id}", response_model=ScreenshotResponse)
@inject
def update_screenshot(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        screenshot_id: str,
        body: UpdateScreenshotBody,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> ScreenshotResponse:
    data = body.model_dump()
    data.pop("created_at", None)
    data.pop("updated_at", None)

    screenshot = screenshot_service.update_screenshot(
        current_user.id,
        screenshot_id,
        **data,
    )
    
    return asdict(screenshot)


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
        category_name: str,
        page: int = 1,
        items_per_page: int = 10,
        screenshot_service: ScreenshotService = Depends(Provide[Container.screenshot_service])
) -> GetScreenshotsResponse:
    total_count, screenshots = screenshot_service.get_screenshot_by_category(
        current_user.id,
        category_name,
        page,
        items_per_page
    )
    response = GetScreenshotsResponse(
        total_count=total_count,
        page=page,
        screenshots=[asdict(screenshot) for screenshot in screenshots]
    )
    return response