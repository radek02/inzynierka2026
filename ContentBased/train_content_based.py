"""
Content-Based Filtering Model Training

Trains a TF-IDF based content similarity model for book recommendations.

USAGE:
    python train_content_based.py

OUTPUT:
    - ../../processed_data/books_filtered.pkl
    - ../../processed_data/tfidf_matrix.pkl
    - ../../processed_data/book_id_to_idx.pkl
"""

import gzip
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Configuration
DATA_DIR = "../../data"
PROCESSED_DATA_DIR = "../../processed_data"
SAMPLE_RATE = 0.1
RANDOM_SEED = 42


def load_data(file_name, sample_rate=0.1, random_seed=42):
    """
    Load data from gzipped JSON file with random sampling.

    Parameters:
    - file_name: path to the file
    - sample_rate: proportion of data to sample (default 0.1 for 10%)
    - random_seed: seed for reproducibility
    """
    np.random.seed(random_seed)
    data = []

    print(f"Loading data from {file_name}...")
    with gzip.open(file_name) as fin:
        for line in fin:
            # Randomly decide whether to include this record
            if np.random.random() < sample_rate:
                d = json.loads(line)
                data.append(d)

    print(f"Loaded {len(data)} books ({sample_rate * 100}% sample)")
    return data


def create_content_features(row):
    """
    Combine multiple features into a single text representation for each book.
    Optimized for memory efficiency.
    """
    features = []

    # Add title (weighted by repeating 2x for importance)
    if pd.notna(row.get("title")):
        title = str(row["title"])
        features.append(title + " " + title)

    # Add authors (weighted by repeating 2x)
    if row.get("authors"):
        author_names = []
        for author in row["authors"][:3]:  # Limit to top 3 authors
            if isinstance(author, dict) and "name" in author:
                author_names.append(author["name"])
        if author_names:
            author_text = " ".join(author_names)
            features.append(author_text + " " + author_text)

    # Add popular shelves (genres) - limit to top 5
    if row.get("popular_shelves"):
        shelves = []
        for shelf in row["popular_shelves"][:5]:  # Reduced from 10 to 5
            if isinstance(shelf, dict) and "name" in shelf:
                shelves.append(shelf["name"].replace("-", " "))
        if shelves:
            features.append(" ".join(shelves))

    return " ".join(features)


def save_processed_data(books_df_filtered, tfidf_matrix, book_id_to_idx, output_dir):
    """Save processed data to disk."""
    os.makedirs(output_dir, exist_ok=True)

    books_path = os.path.join(output_dir, "books_filtered.pkl")
    books_df_filtered.to_pickle(books_path)
    print(f"✓ Saved books: {books_path}")

    tfidf_matrix_path = os.path.join(output_dir, "tfidf_matrix.pkl")
    joblib.dump(tfidf_matrix, tfidf_matrix_path)
    print(f"✓ Saved TF-IDF matrix: {tfidf_matrix_path}")

    book_id_mapping_path = os.path.join(output_dir, "book_id_to_idx.pkl")
    joblib.dump(book_id_to_idx, book_id_mapping_path)
    print(f"✓ Saved book_id mapping: {book_id_mapping_path}")

    total_size = sum(
        os.path.getsize(os.path.join(output_dir, f))
        for f in os.listdir(output_dir)
        if f.endswith(".pkl")
    )
    print(f"\n✓ Total size: {total_size / (1024**2):.2f} MB")


def train_model():
    """
    Main training function.
    """
    print("=" * 80)
    print("CONTENT-BASED FILTERING MODEL TRAINING")
    print("=" * 80)
    print()

    # Load data
    books = load_data(
        os.path.join(DATA_DIR, "goodreads_books.json.gz"),
        sample_rate=SAMPLE_RATE,
        random_seed=RANDOM_SEED,
    )
    books_df = pd.DataFrame(books)
    print(f"DataFrame shape: {books_df.shape}")
    print()

    # Feature Engineering
    print("Creating content features...")
    books_df["content_features"] = books_df.apply(create_content_features, axis=1)

    # Remove books with no content features
    books_df_filtered = books_df[books_df["content_features"].str.len() > 0].copy()
    print(f"Books with valid content features: {len(books_df_filtered)}")

    # Reset index to create clean sequential indices
    books_df_filtered = books_df_filtered.reset_index(drop=True)

    # Create book_id to matrix index mapping
    print("Creating book_id to index mapping...")
    if "book_id" in books_df_filtered.columns:
        book_id_to_idx = {
            book_id: idx for idx, book_id in enumerate(books_df_filtered["book_id"])
        }
        print(f"Created mapping for {len(book_id_to_idx)} book_ids")
    else:
        print("WARNING: 'book_id' column not found in data!")
        print("Available columns:", books_df_filtered.columns.tolist())
        # Try alternative ID columns
        if "work_id" in books_df_filtered.columns:
            print("Using 'work_id' as book identifier instead")
            books_df_filtered["book_id"] = books_df_filtered["work_id"]
            book_id_to_idx = {
                book_id: idx for idx, book_id in enumerate(books_df_filtered["book_id"])
            }
        else:
            raise ValueError("No suitable ID column found in data!")

    print()

    # Build TF-IDF Model
    print("Building TF-IDF model...")
    tfidf = TfidfVectorizer(
        max_features=1000,  # Reduced from 5000 to 1000 for efficiency
        stop_words="english",
        ngram_range=(1, 1),  # Only unigrams (bigrams increase memory significantly)
        min_df=3,  # Increased from 2 to reduce vocabulary size
        max_df=0.7,  # Reduced from 0.8 to filter more common terms
        dtype=np.float32,  # Use float32 instead of float64 to save memory
    )

    tfidf_matrix = tfidf.fit_transform(books_df_filtered["content_features"])
    print(f"✓ TF-IDF matrix shape: {tfidf_matrix.shape}")
    print(f"✓ Number of features: {len(tfidf.get_feature_names_out())}")
    print()

    # Save processed data
    print("Saving processed data...")
    save_processed_data(
        books_df_filtered, tfidf_matrix, book_id_to_idx, PROCESSED_DATA_DIR
    )

    print("\n" + "=" * 80)
    print("TRAINING COMPLETE!")
    print("=" * 80)
    print("\nUse recommend.py to get recommendations by book_id\n")


if __name__ == "__main__":
    train_model()
