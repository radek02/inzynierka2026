import uvicorn
from fastapi import FastAPI
from app.core import settings
from app.api.v1 import recommendations

app = FastAPI(title="Recommendation Service")

app.include_router(recommendations.recommendation_router, prefix="/api/v1/Recommendations", tags=["Recommendations"])

if __name__ == "__main__":   
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)
