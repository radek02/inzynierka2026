"""Content-Based Filtering using TF-IDF for book recommendations."""

import gzip
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DIR = "/Users/rmaksymiuk/MINI/inzynierka/data"
PROCESSED_DATA_DIR = "/Users/rmaksymiuk/MINI/inzynierka/processed_data"

_books_df = None
_tfidf_matrix = None


def _load_data(file_name, sample_rate=0.1, random_seed=42):
    np.random.seed(random_seed)
    data = []
    with gzip.open(file_name) as fin:
        for line in fin:
            if np.random.random() < sample_rate:
                data.append(json.loads(line))
    return data


def _create_content_features(row):
    features = []
    if pd.notna(row.get("title")):
        title = str(row["title"])
        features.append(f"{title} {title}")
    if row.get("authors"):
        names = [
            a["name"] for a in row["authors"][:3] if isinstance(a, dict) and "name" in a
        ]
        if names:
            author_text = " ".join(names)
            features.append(f"{author_text} {author_text}")
    if row.get("popular_shelves"):
        shelves = [
            s["name"].replace("-", " ")
            for s in row["popular_shelves"][:5]
            if isinstance(s, dict) and "name" in s
        ]
        if shelves:
            features.append(" ".join(shelves))
    return " ".join(features)


def _init():
    global _books_df, _tfidf_matrix

    if _books_df is not None:
        return

    paths = [
        os.path.join(PROCESSED_DATA_DIR, "books_filtered.pkl"),
        os.path.join(PROCESSED_DATA_DIR, "tfidf_matrix.pkl"),
        os.path.join(PROCESSED_DATA_DIR, "tfidf_model.pkl"),
    ]

    if all(os.path.exists(p) for p in paths):
        _books_df = pd.read_pickle(paths[0])
        _tfidf_matrix = joblib.load(paths[1])
    else:
        books = _load_data(os.path.join(DIR, "goodreads_books.json.gz"))
        _books_df = pd.DataFrame(books)
        _books_df["content_features"] = _books_df.apply(
            _create_content_features, axis=1
        )
        _books_df = _books_df[_books_df["content_features"].str.len() > 0].copy()

        tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words="english",
            ngram_range=(1, 1),
            min_df=3,
            max_df=0.7,
            dtype=np.float32,
        )
        _tfidf_matrix = tfidf.fit_transform(_books_df["content_features"])

        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        _books_df.to_pickle(paths[0])
        joblib.dump(_tfidf_matrix, paths[1])
        joblib.dump(tfidf, paths[2])


def get_similar_books(book_id, n=10):
    """
    Find similar books given a book_id.

    Returns list of (book_id, similarity_score) tuples, or None if book not found.
    """
    _init()

    matches = _books_df[_books_df["book_id"] == book_id]
    if len(matches) == 0:
        return None

    idx = matches.index[0]
    row_idx = _books_df.index.get_loc(idx)

    similarities = cosine_similarity(_tfidf_matrix[row_idx], _tfidf_matrix).flatten()
    sim_scores = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)[
        1 : n + 1
    ]

    return [(_books_df.iloc[i]["book_id"], float(score)) for i, score in sim_scores]


if __name__ == "__main__":
    _init()
    assert _books_df is not None
    print(f"Loaded {len(_books_df)} books")

    test_id = _books_df["book_id"].iloc[0]
    print(f"\nSimilar books to {test_id}:")
    for bid, score in get_similar_books(test_id, n=5) or []:
        print(f"  {bid}: {score:.3f}")
