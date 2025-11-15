`"""
Example usage of the content-based recommender system.

Demonstrates how to get recommendations by book_id.
"""

from recommend import ContentBasedRecommender, get_recommendations

# Example 1: Using the class (recommended for multiple recommendations)
print("=" * 80)
print("EXAMPLE 1: Using ContentBasedRecommender class")
print("=" * 80)

recommender = ContentBasedRecommender()

# Get recommendations for first book_id in the dataset
book_ids = list(recommender.book_id_to_idx.keys())
if book_ids:
    book_id = book_ids[0]
    print(f"\nGetting recommendations for book_id: {book_id}")

    # Get book info
    idx = recommender.book_id_to_idx[book_id]
    book_info = recommender.books_df.iloc[idx]
    print(f"Title: {book_info.get('title', 'N/A')}")

    # Get recommendations
    recommendations = recommender.get_recommendations(book_id=book_id, n=5)
    print("\nTop 5 recommendations:\n")
    print(recommendations.to_string(index=False))

print("\n")

# Example 2: Using convenience function (simpler but slower for multiple calls)
print("=" * 80)
print("EXAMPLE 2: Using get_recommendations() function")
print("=" * 80)

if len(book_ids) > 1:
    book_id = book_ids[1]
    print(f"\nGetting recommendations for book_id: {book_id}\n")

    recommendations = get_recommendations(book_id=book_id, n=3)
    print(
        recommendations[["book_id", "title", "similarity_score"]].to_string(index=False)
    )

print("\n")

# Example 3: Batch processing
print("=" * 80)
print("EXAMPLE 3: Batch processing multiple books")
print("=" * 80)

if len(book_ids) >= 3:
    for book_id in book_ids[:3]:
        recommendations = recommender.get_recommendations(book_id, n=2)
        print(f"\nTop 2 recommendations for book_id {book_id}:")
        print(
            recommendations[["book_id", "title", "similarity_score"]].to_string(
                index=False
            )
        )

print("\n" + "=" * 80)
print("Examples completed!")
print("=" * 80)
