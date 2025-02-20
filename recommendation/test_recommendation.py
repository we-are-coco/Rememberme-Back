import pytest


from recommendation.application.recommendation_service import RecommendationService

@pytest.fixture
def recommendation_service():
    return RecommendationService()


def test_get_recommendations(recommendation_service):
    # Assuming there are some books in the database that can be recommended
    recommendations = recommendation_service.recommend_coupons()