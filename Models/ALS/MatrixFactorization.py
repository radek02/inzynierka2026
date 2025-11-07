import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
import implicit
import logging
import os


interactions_file = "C:/Users/kegor/Recomendation/Datasets/SmallDirtySets/filtered_every_15th_row.csv"
embedding_dim = 32
saving_directory = 'embeddings/first'

logging.basicConfig(level=logging.INFO)

# Load dataset
print("Loading CSV...")
df = pd.read_csv(interactions_file)

# this will numerate users and items from 0 to N-1, we actually have this kind of numeration, but it still could be
# useful in case we delete some users or items from interaction, after interactions cleaning. This helps to build
# correct coo_matrix, maps from actual ids to new ids of embeddings will be stored in a map file
df["user"] = df["user_id"].astype("category").cat.codes
df["item"] = df["book_id"].astype("category").cat.codes

num_users = df["user"].nunique()
num_items = df["item"].nunique()

print(f"Users: {num_users:,}  |  Books: {num_items:,}  |  Interactions: {len(df):,}")


# Prepare data
ratings_coo = coo_matrix(
    (df["rating"].astype(float), (df["user"], df["item"])),
    shape=(num_users, num_items)
)

ratings_csr = ratings_coo.tocsr()

# Train ALS model
model = implicit.als.AlternatingLeastSquares(
    factors=embedding_dim,
    regularization=0.1,
    iterations=10,
    use_gpu=False
)
os.environ["OPENBLAS_NUM_THREADS"] = "1"

print("Training ALS...")
model.fit(ratings_csr.T.tocsr()) # convert to csr again, because this csr is lost after transposition

# Save embeddings
os.makedirs(saving_directory, exist_ok=True)

np.save(f"{saving_directory}/user_embeddings_{embedding_dim}d.npy", model.user_factors)
np.save(f"{saving_directory}/item_embeddings_{embedding_dim}d.npy", model.item_factors)

# Save mappings to restore ID → embedding relation later
user_id_map = df[["user", "user_id"]].drop_duplicates().sort_values("user")
item_id_map = df[["item", "book_id"]].drop_duplicates().sort_values("item")

user_id_map.to_parquet(f"{saving_directory}/user_id_map.parquet")
item_id_map.to_parquet(f"{saving_directory}/book_id_map.parquet")

print("Training finished.")


