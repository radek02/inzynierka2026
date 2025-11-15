"""
Content-Based Recommendation Module

Get book recommendations by book_id using pre-trained TF-IDF similarity model.

USAGE:
    from recommend import ContentBasedRecommender

    recommender = ContentBasedRecommender()
    recommendations = recommender.get_recommendations(book_id=123456, n=10)
"""

import os

import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

PROCESSED_DATA_DIR = "../../processed_data"


class ContentBasedRecommender:
    """Content-based recommender system using TF-IDF."""

    def __init__(self, data_dir=PROCESSED_DATA_DIR):
        """
        Initialize the recommender by loading the trained model.

        Parameters:
        - data_dir: Directory containing the saved model files
        """
        self._load_model(data_dir)

    def _load_model(self, data_dir):
        """Load the trained model from disk."""
        required_files = [
            "books_filtered.pkl",
            "tfidf_matrix.pkl",
            "book_id_to_idx.pkl",
        ]

        for filename in required_files:
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                raise FileNotFoundError(
                    f"Model file not found: {filepath}\n"
                    f"Run train_content_based.py first to train the model."
                )

        self.books_df = pd.read_pickle(os.path.join(data_dir, "books_filtered.pkl"))
        self.tfidf_matrix = joblib.load(os.path.join(data_dir, "tfidf_matrix.pkl"))
        self.book_id_to_idx = joblib.load(os.path.join(data_dir, "book_id_to_idx.pkl"))
        self.idx_to_book_id = {
            idx: book_id for book_id, idx in self.book_id_to_idx.items()
        }

    def get_recommendations(self, book_id, n=10):
        """
        Get book recommendations based on book_id.

        Parameters:
        - book_id: ID of the book to base recommendations on
        - n: Number of recommendations to return (default: 10)

        Returns:
        - DataFrame with columns: book_id, title, author_names, similarity_score
          Additional columns if available: average_rating, ratings_count, top_genres
        """
        if book_id not in self.book_id_to_idx:
            raise ValueError(
                f"Book ID {book_id} not found in dataset. "
                f"Total books available: {len(self.book_id_to_idx)}"
            )

        # Get matrix index for this book_id
        idx = self.book_id_to_idx[book_id]

        # Compute similarity on-demand (only for this book vs all others)
        book_vector = self.tfidf_matrix[idx]
        similarities = cosine_similarity(book_vector, self.tfidf_matrix).flatten()

        # Get top n+1 similar books (excluding the book itself)
        sim_indices = similarities.argsort()[::-1][1 : n + 1]
        sim_scores = similarities[sim_indices]

        # Create recommendations dataframe
        recommendations = self.books_df.iloc[sim_indices].copy()
        recommendations["book_id"] = [self.idx_to_book_id[i] for i in sim_indices]
        recommendations["similarity_score"] = sim_scores

        # Format output columns
        output_columns = ["book_id", "title", "similarity_score"]

        # Add author names
        if "authors" in recommendations.columns:
            recommendations["author_names"] = recommendations["authors"].apply(
                lambda x: ", ".join(
                    [a.get("name", "Unknown") for a in x if isinstance(a, dict)]
                )
                if x
                else "Unknown"
            )
            output_columns.insert(2, "author_names")

        # Add optional columns if available
        optional_cols = ["average_rating", "ratings_count"]
        for col in optional_cols:
            if col in recommendations.columns:
                output_columns.append(col)

        # Add top genres
        if "popular_shelves" in recommendations.columns:
            recommendations["top_genres"] = recommendations["popular_shelves"].apply(
                lambda x: ", ".join(
                    [s.get("name", "") for s in x[:3] if isinstance(s, dict)]
                )
                if x
                else ""
            )
            output_columns.append("top_genres")

        # Return only relevant columns
        available_columns = [
            col for col in output_columns if col in recommendations.columns
        ]
        return recommendations[available_columns]


def get_recommendations(book_id, n=10, data_dir=PROCESSED_DATA_DIR):
    """
    Convenience function to get recommendations without creating a class instance.

    Note: Creates a new recommender instance each time. For multiple recommendations,
    use ContentBasedRecommender class directly for better performance.

    Parameters:
    - book_id: ID of the book to base recommendations on
    - n: Number of recommendations to return (default: 10)
    - data_dir: Directory containing model files

    Returns:
    - DataFrame with recommendations
    """
    recommender = ContentBasedRecommender(data_dir)
    return recommender.get_recommendations(book_id, n)
