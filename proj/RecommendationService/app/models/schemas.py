from pydantic import BaseModel
from typing import List

class UserRecmmendationResponse(BaseModel):
    user_id: int
    recommended_books: List[int]