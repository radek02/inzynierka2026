from unittest.mock import MagicMock, Mock

import pytest
from app.db import CacheRecommendationRepository, InteractionsRepository
from app.models import Book, Interaction


class TestInteractionsRepository:
    def test_insert_success(self):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 10, 20, 5)
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        repo = InteractionsRepository(mock_db)
        result = repo.insert_new_interaction(user_id=10, book_id=20, rating=5)

        assert result == Interaction(id=1, user_id=10, book_id=20, rating=5)
        mock_db.commit.assert_called_once()

    def test_insert_rollback_on_exception(self):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB error")
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        repo = InteractionsRepository(mock_db)

        with pytest.raises(Exception):
            repo.insert_new_interaction(user_id=10, book_id=20, rating=5)

        mock_db.rollback.assert_called_once()


class TestCacheRecommendationRepository:
    def test_get_cache_hit(self):
        mock_cache = Mock()
        mock_cache.get.return_value = '[{"book_id": 1}]'

        repo = CacheRecommendationRepository(mock_cache, ttl=3600)
        result = repo.try_get_user_recommendation(user_id=1)

        assert result == [Book(book_id=1)]

    def test_get_cache_miss(self):
        mock_cache = Mock()
        mock_cache.get.return_value = None

        repo = CacheRecommendationRepository(mock_cache, ttl=3600)
        result = repo.try_get_user_recommendation(user_id=1)

        assert result is None

    def test_delete(self):
        mock_cache = Mock()

        repo = CacheRecommendationRepository(mock_cache, ttl=3600)
        repo.delete_user_recommendation(user_id=1)

        mock_cache.delete.assert_called_once_with("recommendations:user:1")
