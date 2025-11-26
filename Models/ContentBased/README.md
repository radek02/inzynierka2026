# Content-Based Filtering

TF-IDF based book similarity using title, authors, and genres.

## Usage

```python
from content_based import get_similar_books

similar = get_similar_books("12345", n=10)
# Returns: [("book_id_1", 0.85), ("book_id_2", 0.72), ...]
```
