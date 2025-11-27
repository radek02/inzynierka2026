import argparse
import logging
import os

import implicit
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_file", required=True, help="Path to goodreads_interactions.csv"
)
args = parser.parse_args()

embedding_dim = 32
saving_directory = "Models/ALS/embeddings/full2"

logging.basicConfig(level=logging.INFO)

# Load dataset
print(f"Loading {args.input_file}...")
df = pd.read_csv(args.input_file)

# this will numerate users and items from 0 to N-1, we actually have this kind of numeration, but it still could be
# useful in case we delete some users or items from interaction, after interactions cleaning. This helps to build
# correct coo_matrix, maps from actual ids to new ids of embeddings will be stored in a map file
df["user"] = df["user_id"].astype("category").cat.codes
df["book"] = df["book_id"].astype("category").cat.codes

num_users = df["user"].nunique()
num_items = df["book"].nunique()

print(f"Users: {num_users:,}  |  Books: {num_items:,}  |  Interactions: {len(df):,}")


# Prepare data
ratings_coo = coo_matrix(
    (df["rating"].astype(float), (df["user"], df["book"])), shape=(num_users, num_items)
)

ratings_csr = ratings_coo.tocsr()

# Train ALS model
model = implicit.als.AlternatingLeastSquares(
    factors=embedding_dim, regularization=0.1, iterations=10, use_gpu=False
)
os.environ["OPENBLAS_NUM_THREADS"] = "1"

print("Training ALS...")
model.fit(ratings_csr)

# Save embeddings
os.makedirs(saving_directory, exist_ok=True)

np.save(f"{saving_directory}/user_embeddings_{embedding_dim}d.npy", model.user_factors)
np.save(f"{saving_directory}/book_embeddings_{embedding_dim}d.npy", model.item_factors)

# Save mappings to restore ID → embedding relation later
user_id_map = (
    df[["user", "user_id"]].drop_duplicates().sort_values("user")
)  # index_csv -> index_als user = index_als | user_id = index_csv
item_id_map = df[["book", "book_id"]].drop_duplicates().sort_values("book")

user_id_map.to_parquet(f"{saving_directory}/user_id_map.parquet")
item_id_map.to_parquet(f"{saving_directory}/book_id_map.parquet")

print("Training finished.")
