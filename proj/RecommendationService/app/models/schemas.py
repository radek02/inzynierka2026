from typing import List

from pydantic import BaseModel


class UserRecommendationResponse(BaseModel):
    user_id: int
    recommended_books: List[int]