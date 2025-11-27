"""Test ALS recommendations without infrastructure."""

import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument(
    "--user_id", required=True, type=int, help="User ID to get recommendations for"
)
args = parser.parse_args()

EMBEDDINGS_DIR = "Models/ALS/embeddings/full2"

# Load embeddings and mappings
user_emb = np.load(f"{EMBEDDINGS_DIR}/user_embeddings_32d.npy")
book_emb = np.load(f"{EMBEDDINGS_DIR}/book_embeddings_32d.npy")
user_map = pd.read_parquet(f"{EMBEDDINGS_DIR}/user_id_map.parquet")
book_map = pd.read_parquet(f"{EMBEDDINGS_DIR}/book_id_map.parquet")

print(f"Users: {len(user_emb)}, Books: {len(book_emb)}")


def get_recommendations(user_id, n=10):
    """Get top N book recommendations for a user."""
    # Find user's embedding index
    user_row = user_map[user_map["user_id"] == user_id]
    if user_row.empty:
        return None
    user_idx = user_row["user"].values[0]

    # Compute dot product with all books
    user_vec = user_emb[user_idx]
    scores = book_emb @ user_vec

    # Get top N book indices
    top_indices = np.argsort(scores)[-n:][::-1]

    # Map back to book_ids
    results = []
    for idx in top_indices:
        book_row = book_map[book_map["book"] == idx]
        if not book_row.empty:
            book_id = book_row["book_id"].values[0]
            results.append((book_id, float(scores[idx])))

    return results


results = get_recommendations(args.user_id, n=10)
if results is None:
    print(f"User {args.user_id} not found")
else:
    print(f"\nRecommendations for user {args.user_id}:")
    for book_id, score in results:
        print(f"  Book {book_id}: {score:.4f}")
