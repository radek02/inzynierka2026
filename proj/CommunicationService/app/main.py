import uvicorn
from fastapi import FastAPI

from app.api.v1 import (
    interactions_router,
    recommendations_router,
    similar_router,
)
from app.core import settings

app = FastAPI(
    title="Book Recommendation Communication Service",
    description="Service Module from lab2 specification",
    version="1.0.0",
)

# Include routers
app.include_router(recommendations_router, prefix="/api/v1", tags=["Recommendations"])
app.include_router(interactions_router, prefix="/api/v1", tags=["Interactions"])
app.include_router(similar_router, prefix="/api/v1", tags=["Similar Books"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)
