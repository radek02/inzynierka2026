from unittest.mock import MagicMock, Mock

import pytest
from app.db import InteractionsRepository
from app.models import Interaction


class TestInteractionsRepository:
    def test_get_user_interactions_success(self):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, 10, 5),
            (1, 20, 4),
        ]
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        repo = InteractionsRepository(mock_db)
        result = repo.get_user_interactions(user_id=1)

        assert len(result) == 2
        assert result[0].user_id == 1
        assert result[0].book_id == 10
        assert result[0].rating == 5

    def test_get_user_interactions_empty(self):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        repo = InteractionsRepository(mock_db)
        result = repo.get_user_interactions(user_id=999)

        assert result == []


class TestQdrantEmbeddingsStorage:
    def test_get_user_embeddings_success(self):
        from app.db import QdrantEmbeddingsStorage

        mock_point = Mock()
        mock_point.vector = [0.1, 0.2, 0.3]

        storage = QdrantEmbeddingsStorage.__new__(QdrantEmbeddingsStorage)
        storage.client = Mock()
        storage.client.retrieve.return_value = [mock_point]

        result = storage.get_user_embeddings(user_id=1)

        assert result == [0.1, 0.2, 0.3]
        storage.client.retrieve.assert_called_once()

    def test_get_user_embeddings_not_found(self):
        from app.db import QdrantEmbeddingsStorage

        storage = QdrantEmbeddingsStorage.__new__(QdrantEmbeddingsStorage)
        storage.client = Mock()
        storage.client.retrieve.return_value = []

        with pytest.raises(ValueError, match="not found"):
            storage.get_user_embeddings(user_id=999)
