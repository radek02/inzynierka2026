"""Visualization of Content-Based model feature importance."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

PROCESSED_DATA_DIR = "/Users/rmaksymiuk/MINI/inzynierka/processed_data"

sns.set_style("whitegrid")


def _load_model():
    books_df = pd.read_pickle(os.path.join(PROCESSED_DATA_DIR, "books_filtered.pkl"))
    tfidf_matrix = joblib.load(os.path.join(PROCESSED_DATA_DIR, "tfidf_matrix.pkl"))
    tfidf = joblib.load(os.path.join(PROCESSED_DATA_DIR, "tfidf_model.pkl"))
    return books_df, tfidf_matrix, tfidf


def plot_top_features(tfidf, tfidf_matrix, n=20):
    """Plot top N TF-IDF features by average score."""
    feature_names = tfidf.get_feature_names_out()
    feature_scores = np.array(tfidf_matrix.mean(axis=0)).flatten()
    top_idx = feature_scores.argsort()[-n:][::-1]

    df = pd.DataFrame({
        "Feature": [feature_names[i] for i in top_idx],
        "Score": [feature_scores[i] for i in top_idx],
    })

    plt.figure(figsize=(10, 8))
    plt.barh(range(len(df)), df["Score"], color="steelblue")
    plt.yticks(range(len(df)), df["Feature"])
    plt.xlabel("Average TF-IDF Score")
    plt.title(f"Top {n} Most Important Content Features")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    return df


def plot_feature_distribution(tfidf_matrix):
    """Plot distribution of non-zero TF-IDF values."""
    plt.figure(figsize=(10, 5))
    plt.hist(tfidf_matrix.data, bins=50, color="steelblue", edgecolor="white")
    plt.xlabel("TF-IDF Score")
    plt.ylabel("Frequency")
    plt.title("Distribution of Non-Zero TF-IDF Values")
    plt.tight_layout()
    plt.show()


def plot_sparsity_info(tfidf_matrix):
    """Plot sparsity information of TF-IDF matrix."""
    n_elements = tfidf_matrix.shape[0] * tfidf_matrix.shape[1]
    n_nonzero = tfidf_matrix.nnz
    sparsity = 1 - (n_nonzero / n_elements)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].pie(
        [n_nonzero, n_elements - n_nonzero],
        labels=["Non-zero", "Zero"],
        autopct="%1.2f%%",
        colors=["steelblue", "lightgray"],
    )
    axes[0].set_title("Matrix Sparsity")

    stats = {
        "Books": tfidf_matrix.shape[0],
        "Features": tfidf_matrix.shape[1],
        "Non-zero values": n_nonzero,
        "Sparsity": f"{sparsity:.2%}",
    }
    axes[1].axis("off")
    text = "\n".join([f"{k}: {v:,}" if isinstance(v, int) else f"{k}: {v}" for k, v in stats.items()])
    axes[1].text(0.3, 0.5, text, fontsize=14, verticalalignment="center", fontfamily="monospace")
    axes[1].set_title("Matrix Statistics")

    plt.tight_layout()
    plt.show()


def plot_books_per_feature_count(tfidf_matrix):
    """Plot how many features each book has (non-zero count per row)."""
    features_per_book = np.diff(tfidf_matrix.indptr)

    plt.figure(figsize=(10, 5))
    plt.hist(features_per_book, bins=50, color="steelblue", edgecolor="white")
    plt.xlabel("Number of Features per Book")
    plt.ylabel("Number of Books")
    plt.title("Distribution of Feature Count per Book")
    plt.axvline(features_per_book.mean(), color="red", linestyle="--", label=f"Mean: {features_per_book.mean():.1f}")
    plt.legend()
    plt.tight_layout()
    plt.show()


def generate_all_visualizations():
    """Generate all visualizations for the content-based model."""
    print("Loading model...")
    books_df, tfidf_matrix, tfidf = _load_model()
    print(f"Loaded {len(books_df)} books, {tfidf_matrix.shape[1]} features\n")

    print("1. Top Features")
    top_df = plot_top_features(tfidf, tfidf_matrix, n=20)
    print(top_df.to_string(index=False))

    print("\n2. TF-IDF Distribution")
    plot_feature_distribution(tfidf_matrix)

    print("\n3. Matrix Sparsity")
    plot_sparsity_info(tfidf_matrix)

    print("\n4. Features per Book")
    plot_books_per_feature_count(tfidf_matrix)


if __name__ == "__main__":
    generate_all_visualizations()
