from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from dependency_injector.wiring import inject
from utils.ai import extract_data_from_screenshots
from utils.infer import infer
from dataclasses import asdict, dataclass

@dataclass
class Recommendation:
    id: str # screenshot_id
    is_reco: bool
    reco_date: str | None
    reco_time: str | None
    item: str | None
    description: str | None

class RecommendationService:
    @inject
    def __init__(self, screenshot_repo: IScreenshotRepository):
        self.screenshot_repo = screenshot_repo

    def recommend_coupons(self, user_id: str, days: int) -> list:
        total, screenshots = self.screenshot_repo.get_screenshots(user_id=user_id, keywords=None, unused_only=True)
        data = extract_data_from_screenshots([asdict(screenshot) for screenshot in screenshots])
        results = infer(data, days)

        screenshot_dict = {screenshot.id: screenshot for screenshot in screenshots}
        coupons = [ {
            "screenshot_id": result["id"],
            "brand": screenshot_dict[result["id"]].get("brand", None),
            "is_reco": result["is_reco"],
            "reco_date": result.get("reco_date", None),
            "reco_time": result.get("reco_time", None),
            "item": result.get('item', None),
            "description": result.get("description", None)
        } for result in results]
        return coupons

