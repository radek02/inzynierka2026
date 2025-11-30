import uvicorn
from fastapi import FastAPI
from app.core import settings
from app.api.v1 import recommendations
from contextlib import asynccontextmanager
from app.core.dependency_container import init_mf_model_service, init_model_loader
from app.ml_models import IMFModelService

mf_model_service: IMFModelService = init_mf_model_service(model_loader=init_model_loader(settings))

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading MF model")
    mf_model_service.load_model()
    app.state.mf_model_service = mf_model_service
    print ("MF model loaded")
    
    yield

    print("Shutting down... clearing MF model from memory.")
    app.state.mf_model_service = None

app = FastAPI(title="Recommendation Service", lifespan=lifespan)

app.include_router(recommendations.recommendation_router, prefix="/api/v1/Recommendations", tags=["Recommendations"])

if __name__ == "__main__":   
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)
