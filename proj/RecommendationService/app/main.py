import uvicorn
from fastapi import FastAPI
from app.core import settings

app = FastAPI(title="Recommendation Service")

if __name__ == "__main__":   
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)
