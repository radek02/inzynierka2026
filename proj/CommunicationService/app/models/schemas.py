from pydantic import BaseModel, Field


# helper classes
class Book(BaseModel):
    book_id: int


# Recommendations endpoint (GET)
class RecommendationsRequest(BaseModel):
    user_id: int = Field(gt=0, description="User ID")


class Recommendation(BaseModel):
    user_id: int
    books: list[Book]
    source: str  # cache vs computed


class RecommendationsResponse(BaseModel):
    recommendation: Recommendation


# Similar endpoint (GET)
class SimilarRequest(BaseModel):
    book_id: int = Field(gt=0, description="Book ID")


class SimilarResponse(BaseModel):
    book_id: int
    similar_books: list[Book]


# Interactions endpoint (POST)
class Interaction(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int


class InteractionsRequest(BaseModel):
    user_id: int = Field(gt=0, description="User ID")
    book_id: int = Field(gt=0, description="Book ID")
    rating: int = Field(ge=0, le=5, description="Rating 0-5")


class InteractionsResponse(BaseModel):
    message: str
    interaction: Interaction


# Error
class ErrorResponse(BaseModel):
    detail: str
