import httpx


class RecommendationServiceClient:
    """HTTP client for RecommendationService"""

    def __init__(self, base_url: str, timeout: float):
        self.base_url = base_url
        self.timeout = timeout

    def get_user_recommendations(self, user_id: int) -> list[int]:
        url = f"{self.base_url}/api/v1/Recommendations/user-recommendations/{user_id}"

        try:
            response = httpx.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            return data.get("recommended_books", [])

        except httpx.HTTPError as e:
            raise Exception(f"Failed to get recommendations: {str(e)}")
