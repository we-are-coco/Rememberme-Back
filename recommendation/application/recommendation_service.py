from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from dependency_injector.wiring import inject
from utils.ai import extract_data_from_screenshots
from utils.infer import infer
from dataclasses import asdict

class RecommendationService:
    @inject
    def __init__(self, screenshot_repo: IScreenshotRepository):
        self.screenshot_repo = screenshot_repo

    def recommend_coupons(self, user_id: str, days: int) -> list:
        total, screenshots = self.screenshot_repo.get_screenshots(user_id=user_id, keywords=None, unused_only=True)
        data = extract_data_from_screenshots([asdict(screenshot) for screenshot in screenshots])
        results = infer(data, days)
        return results
