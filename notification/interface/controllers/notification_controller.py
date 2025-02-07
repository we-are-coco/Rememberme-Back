from dataclasses import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from typing import Annotated
from common.auth import CurrentUser, get_current_user
from containers import Container
from notification.application.notification_service import NotificationService
from datetime import datetime

router = APIRouter(prefix="/notification")


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    screenshot_id: str
    notification_time: datetime
    is_sent: bool
    created_at: datetime
    updated_at: datetime


@router.post("/{screenshot_id}", status_code=201, response_model=NotificationResponse)
@inject
def create_notification(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        screenshot_id: str,
        notification_time: datetime,
        notification_service: NotificationService = Depends(Provide[Container.notification_service])
) -> NotificationResponse:
    """ 특정 스크린샷에 대한 알림을 생성 """
    notification = notification_service.create_notification(
        user_id=current_user.id,
        screenshot_id=screenshot_id,
        notification_time=notification_time
    )
    response = asdict(notification)
    return response


class GetNotificationsResponse(BaseModel):
    total_count: int
    page: int
    notifications: list[NotificationResponse]


@router.get("", response_model=GetNotificationsResponse)
@inject
def get_notifications(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        page: int = 1,
        items_per_page: int = 10,
        notification_service: NotificationService = Depends(Provide[Container.notification_service])
) -> GetNotificationsResponse:
    """ 사용자의 모든 알림 조회 """
    total_count, notifications = notification_service.get_notifications(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page
    )
    response = GetNotificationsResponse(
        total_count=total_count,
        page=page,
        notifications=[asdict(notification) for notification in notifications]
    )
    return response


@router.get("/{notification_id}", response_model=NotificationResponse)
@inject
def get_notification(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        notification_id: str,
        notification_service: NotificationService = Depends(Provide[Container.notification_service])
) -> NotificationResponse:
    """ 특정 알림 조회 """
    notification = notification_service.get_notification(
        user_id=current_user.id,
        notification_id=notification_id
    )
    response = asdict(notification)
    return response


@router.delete("/{notification_id}", status_code=204)
@inject
def delete_notification(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        notification_id: str,
        notification_service: NotificationService = Depends(Provide[Container.notification_service])
):
    """ 특정 알림 삭제 """
    notification_service.delete_notification(
        user_id=current_user.id,
        notification_id=notification_id
    )


@router.put("/{notification_id}/mark-as-sent", response_model=NotificationResponse)
@inject
def mark_notification_as_sent(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        notification_id: str,
        notification_service: NotificationService = Depends(Provide[Container.notification_service])
) -> NotificationResponse:
    """ 특정 알림을 '보낸 상태'로 변경 """
    notification = notification_service.mark_notification_as_sent(
        user_id=current_user.id,
        notification_id=notification_id
    )
    response = asdict(notification)
    return response