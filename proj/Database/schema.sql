-- Database schema for Book Recommendation System
-- User-book interactions table

CREATE TABLE IF NOT EXISTS user_book_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_book UNIQUE(user_id, book_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_interactions ON user_book_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_book_interactions ON user_book_interactions(book_id);
CREATE INDEX IF NOT EXISTS idx_created_at ON user_book_interactions(created_at);

-- Optional: Create a view for basic statistics
CREATE OR REPLACE VIEW interaction_stats AS
SELECT
    COUNT(*) as total_interactions,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT book_id) as unique_books,
    AVG(rating) as avg_rating,
    MIN(created_at) as earliest_interaction,
    MAX(created_at) as latest_interaction
FROM user_book_interactions;
