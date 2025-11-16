import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Load environment variables from .env file in CommunicationService/
load_dotenv()

app = FastAPI(title="Example API")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "message": "Item created successfully"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    host = os.getenv("FASTAPI_HOST", "localhost")
    port = int(os.getenv("FASTAPI_PORT", "8000"))

    uvicorn.run(app, host=host, port=port)
