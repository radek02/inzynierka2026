# Content-Based Filtering Recommender

A simple TF-IDF based book recommendation system that provides recommendations by book_id.

## 📁 Files

```
Models/ContentBased/
├── train_content_based.py   # Train the model
├── recommend.py              # Get recommendations by book_id
├── example_usage.py          # Usage examples
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Train the Model (First Time Only)

```bash
cd Models/ContentBased
python train_content_based.py
```

This creates:
- `../../processed_data/books_filtered.pkl`
- `../../processed_data/tfidf_matrix.pkl`
- `../../processed_data/book_id_to_idx.pkl`

### 2. Get Recommendations

```python
from recommend import ContentBasedRecommender

# Initialize (loads model automatically)
recommender = ContentBasedRecommender()

# Get recommendations by book_id
recommendations = recommender.get_recommendations(book_id=123456, n=10)
print(recommendations)
```

**Output:**
```
book_id                              title           author_names  similarity_score
  78901  Similar Book Title              Author Name          0.85
  45678  Another Recommendation          Another Author       0.82
  ...
```

## 📊 API Reference

### ContentBasedRecommender

```python
recommender = ContentBasedRecommender(data_dir="../../processed_data")
```

**Methods:**

#### `get_recommendations(book_id, n=10)`
Get n most similar books to the given book_id.

**Parameters:**
- `book_id` (int): ID of the book to base recommendations on
- `n` (int): Number of recommendations to return (default: 10)

**Returns:**
- `pandas.DataFrame` with columns:
  - `book_id`: Recommended book ID
  - `title`: Book title
  - `author_names`: Author(s)
  - `similarity_score`: Similarity score (0-1)
  - `average_rating`: Average rating (if available)
  - `ratings_count`: Number of ratings (if available)
  - `top_genres`: Top 3 genres (if available)

**Raises:**
- `ValueError`: If book_id not found in dataset

### Convenience Function

```python
from recommend import get_recommendations

# Quick one-liner (loads model each time - slower for multiple calls)
recs = get_recommendations(book_id=123456, n=10)
```

## 💡 Usage Examples

### Single Recommendation

```python
from recommend import ContentBasedRecommender

recommender = ContentBasedRecommender()
recs = recommender.get_recommendations(book_id=123456, n=5)

for _, book in recs.iterrows():
    print(f"{book['title']} by {book['author_names']}")
    print(f"  Similarity: {book['similarity_score']:.2%}\n")
```

### Batch Processing

```python
# Get recommendations for multiple books efficiently
recommender = ContentBasedRecommender()

book_ids = [123, 456, 789]
for book_id in book_ids:
    recs = recommender.get_recommendations(book_id, n=3)
    print(f"Recommendations for book {book_id}:")
    print(recs[['book_id', 'title', 'similarity_score']])
```

### Integration Example (Web API)

```python
from flask import Flask, jsonify
from recommend import ContentBasedRecommender

app = Flask(__name__)

# Load model once at startup
recommender = ContentBasedRecommender()

@app.route('/recommendations/<int:book_id>')
def get_recs(book_id):
    try:
        recs = recommender.get_recommendations(book_id, n=10)
        return jsonify(recs.to_dict(orient='records'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run()
```

## 🔧 Configuration

Edit `train_content_based.py` to adjust:

```python
SAMPLE_RATE = 0.1        # Percentage of data to use (0.1 = 10%)
RANDOM_SEED = 42         # For reproducibility
```

TF-IDF parameters:
```python
TfidfVectorizer(
    max_features=1000,    # Number of features
    stop_words="english", # Remove common words
    min_df=3,             # Min document frequency
    max_df=0.7,           # Max document frequency
)
```

## 🔄 Retraining

To retrain with different parameters:

```bash
# Delete cached model
rm -rf ../../processed_data/

# Modify train_content_based.py parameters

# Retrain
python train_content_based.py
```

## ⚡ Performance

- **Training**: ~1-2 minutes (10% sample)
- **Loading**: ~2-5 seconds
- **Recommendation**: ~0.1 seconds per book
- **Memory**: ~50-100 MB (10% sample)

## 🐛 Troubleshooting

### "Model file not found"
**Solution:** Run `python train_content_based.py` first

### "Book ID not found"
**Solution:** Use a valid book_id from your dataset. Check available book_ids:
```python
recommender = ContentBasedRecommender()
print(list(recommender.book_id_to_idx.keys())[:10])  # Show first 10
```

## 🎯 Use Cases

This recommender is designed to be part of a broader recommendation system where:
- Users view/interact with books by book_id
- You need fast, content-based recommendations
- You want to find similar books based on title, author, and genre
- You're building a hybrid recommender that combines multiple approaches

## 📝 Notes

- Recommendations are based on TF-IDF similarity of book metadata (title, authors, genres)
- Does not use user behavior or ratings
- Ideal for "books similar to this one" features
- Can be combined with collaborative filtering for hybrid recommendations
