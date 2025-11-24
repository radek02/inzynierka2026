from .interfaces import IEmbeddingsStorage
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core import AppConfig
from typing import List
from app.models import GeneratedCandidate

USER_COLLECTOION = "users"
BOOK_COLLECTION = "books"

class QdrantEmbeddingsStorage(IEmbeddingsStorage):
    def __init__(self, settings: AppConfig):
        url = settings.qdrant_url
        self.client = QdrantClient(url = url)

    def get_user_embeddings(self, user_id: int) -> List[float]:
        result = self.client.retrieve(
            collection_name=USER_COLLECTOION,
            ids=[user_id],
            with_vectors=True
        )

        if not result:
            raise ValueError(f"User {user_id} not found")

        return result[0].vector


    def get_best_books(self, user_embeddings: List[float], amount: int) -> List[GeneratedCandidate]:
        search_results = self.client.query_points(
            collection_name=BOOK_COLLECTION,
            query=user_embeddings, 
            limit=amount,
            with_vectors=True
        )
            
        return [
            GeneratedCandidate(
                book_id=hit.id,            
                book_embeddings=hit.vector,
                score=hit.score            
            )
            for hit in search_results.points
        ]


    def update_user_embeddings(self, user_id: int, new_embeddings: List[float]):
        self.client.update_vectors(
            collection_name=USER_COLLECTOION,
            points=[
                models.PointVectors(
                    id=user_id,
                    vector={
                        "image": new_embeddings,
                    },
                )
            ],
        )