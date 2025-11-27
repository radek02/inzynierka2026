"""Test content-based similar books."""

import argparse

import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

parser = argparse.ArgumentParser()
parser.add_argument("--book_id", required=True, help="Book ID to find similar books for")
args = parser.parse_args()

EMBEDDINGS_DIR = "Models/ContentBased/output"

books_df = pd.read_pickle(f"{EMBEDDINGS_DIR}/books_df.pkl")
tfidf_matrix = joblib.load(f"{EMBEDDINGS_DIR}/tfidf_matrix.pkl")

print(f"Books: {len(books_df)}")

matches = books_df[books_df["book_id"] == args.book_id]
if len(matches) == 0:
    print(f"Book {args.book_id} not found")
else:
    idx = matches.index[0]
    row_idx = books_df.index.get_loc(idx)

    similarities = cosine_similarity(tfidf_matrix[row_idx], tfidf_matrix).flatten()
    sim_scores = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)[1:11]

    print(f"\nSimilar books to {args.book_id}:")
    for i, score in sim_scores:
        print(f"  {books_df.iloc[i]['book_id']}: {score:.4f}")
