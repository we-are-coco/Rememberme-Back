from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from typing import Annotated
from pydantic import BaseModel
from recommendation.application.recommendation_service import RecommendationService
from common.auth import CurrentUser, get_current_user
from containers import Container


router = APIRouter(prefix="/recommendations")


class RecommendationResponse(BaseModel):
    screenshot_id: str
    is_reco: bool
    reco_date: str | None
    reco_time: str | None
    item: str | None
    brand: str | None
    description: str | None


@router.post("/coupon", response_model=list[RecommendationResponse])
@inject
def recommend_coupon(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: RecommendationService = Depends(Provide[Container.recommendation_service]),
    days: int = 30,
):
    return service.recommend_coupons(current_user.id, days)