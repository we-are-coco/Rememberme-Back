from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel
from recommendation.application.recommendation_service import RecommendationService
from common.auth import CurrentUser, get_current_user
from datetime import datetime

router = APIRouter(prefix="/recommendations")


class RecommendationResponse(BaseModel):
    id: str
    title: str
    screenshot_id: str


@router.post("/coupon", response_model=RecommendationResponse)
def recommend_coupon(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    start_date: datetime,
    end_date: datetime,
):
    service = RecommendationService()

    return service.recommend_coupons(current_user.id, start_date, end_date)