from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Dict, List, Generator
from interfaces import IVectorRepository

qdrant_collections = ["users", "books"]

class QdrantRepository(IVectorRepository):
    def __init__(self, url: str):
        self.client = QdrantClient(url=url)

    def _batch(self, iterable, size: int) -> Generator:
        for i in range(0, len(iterable), size):
            yield iterable[i:i+size]

    def recreate_collection(self, dim: int):
        my_hnsw_config = models.HnswConfigDiff(on_disk=False)
        my_optimizers_config = models.OptimizersConfigDiff(default_segment_number=1)
        my_vectors_params = models.VectorParams(size=dim, distance=models.Distance.DOT)

        for name in qdrant_collections:
            self.client.recreate_collection(
                collection_name=name,
                vectors_config=my_vectors_params,
                hnsw_config=my_hnsw_config,
                optimizers_config=my_optimizers_config
            )
            print(f"Recreated collection: {name}")
    
    def upload_vectors(self, collection_name, data, id_map, batch_size):
        for idx_batch in self._batch(range(len(data)), batch_size):
            self.client.upsert(
                collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=int(id_map[i]),
                    vector=data[i]  
                )
                for i in idx_batch
            ]
            )
    
    def create_indexing(self, collection_name):
        self.client.update_collection(
            collection_name,
            optimizers_config=models.OptimizersConfigDiff(indexing_threshold=20000)
        )
        print(f"Indexing created for {collection_name}")