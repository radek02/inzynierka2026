"""Train TF-IDF model for content-based filtering."""

import argparse
import gzip
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", required=True, help="Path to goodreads_books.json.gz")
args = parser.parse_args()

SAVING_DIRECTORY = "Models/ContentBased/output"


def _load_data(file_name):
    data = []
    with gzip.open(file_name) as fin:
        for line in fin:
            data.append(json.loads(line))
    return data


def _create_content_features(row):
    features = []
    if pd.notna(row.get("title")):
        title = str(row["title"])
        features.append(f"{title} {title}")
    if row.get("authors"):
        names = [a["name"] for a in row["authors"][:3] if isinstance(a, dict) and "name" in a]
        if names:
            features.append(f"{' '.join(names)} {' '.join(names)}")
    if row.get("popular_shelves"):
        shelves = [s["name"].replace("-", " ") for s in row["popular_shelves"][:5]
                   if isinstance(s, dict) and "name" in s]
        if shelves:
            features.append(" ".join(shelves))
    return " ".join(features)


print(f"Loading {args.input_file}...")
books_df = pd.DataFrame(_load_data(args.input_file))
books_df["content_features"] = books_df.apply(_create_content_features, axis=1)
books_df = books_df[books_df["content_features"].str.len() > 0].copy()

print(f"Books: {len(books_df):,}")

tfidf = TfidfVectorizer(max_features=1000, stop_words="english", ngram_range=(1, 1),
                        min_df=3, max_df=0.7, dtype=np.float32)
tfidf_matrix = tfidf.fit_transform(books_df["content_features"])

os.makedirs(SAVING_DIRECTORY, exist_ok=True)
books_df.to_pickle(f"{SAVING_DIRECTORY}/books_df.pkl")
joblib.dump(tfidf_matrix, f"{SAVING_DIRECTORY}/tfidf_matrix.pkl")

print("Training finished.")
