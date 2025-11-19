import numpy as np 
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http import models

# ------------------------
# Data preparation
# ------------------------
user_embeddings_path = "C:/Users/kegor/Recomendation/Models/ALS/embeddings/first/user_embeddings_32d.npy"
book_embeddings_path = "C:/Users/kegor/Recomendation/Models/ALS/embeddings/first/item_embeddings_32d.npy"

user_mapping_path = "C:/Users/kegor/Recomendation/Models/ALS/embeddings/first/user_id_map.parquet"
book_mapping_path = "C:/Users/kegor/Recomendation/Models/ALS/embeddings/first/book_id_map.parquet"

user_embeddings = np.load(user_embeddings_path)
book_embeddings = np.load(book_embeddings_path)

user_mapping = pd.read_parquet(user_mapping_path)
book_mapping = pd.read_parquet(book_mapping_path)

user_id_map = dict(zip(user_mapping["user"], user_mapping["user_id"]))
book_id_map = dict(zip(book_mapping["item"], book_mapping["book_id"]))

# -----------------------
# Qdrant connection
# -----------------------

client = QdrantClient(
    url="http://localhost:6333"
)

# -----------------------
# Collection creation
# -----------------------

DIM = 32

# Books cllection (searc-heavy)
client.recreate_collection(
    collection_name="books",
    vectors_config=models.VectorParams(
        size=DIM,
        distance=models.Distance.DOT
    ),
    hnsw_config=models.HnswConfigDiff(on_disk=False),
    optimizers_config=models.OptimizersConfigDiff(
        default_segment_number=1,
        indexing_threshold=0  
    )
)

# Users collection
client.recreate_collection(
    collection_name="users",
    vectors_config=models.VectorParams(
        size=DIM,
        distance=models.Distance.DOT
    ),
    hnsw_config=models.HnswConfigDiff(on_disk=False),
    optimizers_config=models.OptimizersConfigDiff(
        default_segment_number=1,
        indexing_threshold=0 
    )
)

# -----------------------
# Upload data
# -----------------------
BATCH_SIZE = 10000

def batch(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i+size]

for idx_batch in batch(range(len(book_embeddings)), BATCH_SIZE):
    client.upsert(
        collection_name="books",
        points=[
            models.PointStruct(
                id=int(book_id_map[i]),
                vector=book_embeddings[i].tolist()
            )
            for i in idx_batch
        ]
    )

for idx_batch in batch(range(len(user_embeddings)), BATCH_SIZE):
    client.upsert(
        collection_name="users",
        points=[
            models.PointStruct(
                id=int(user_id_map[i]),
                vector=user_embeddings[i].tolist()
            )
            for i in idx_batch
        ]
    )

# -----------------------
# Create indexes
# -----------------------
client.update_collection(
    "books",
    optimizers_config=models.OptimizersConfigDiff(indexing_threshold=20000)
)

client.update_collection(
    "users",
    optimizers_config=models.OptimizersConfigDiff(indexing_threshold=20000)
)

