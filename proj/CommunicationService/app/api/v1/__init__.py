from .endpoints.interactions import router as interactions_router
from .endpoints.recommendations import router as recommendations_router
from .endpoints.similar import router as similar_router

__all__ = [
    "recommendations_router",
    "interactions_router",
    "similar_router",
]
