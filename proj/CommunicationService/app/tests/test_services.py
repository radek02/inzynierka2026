from unittest.mock import Mock

import pytest
from app.models import Book, Interaction
from app.services import InteractionsService, RecommendationService
from app.services.interactions_service import InteractionError


class TestInteractionsService:
    def test_register_interaction_success(self):
        mock_interactions_repo = Mock()
        mock_cache_repo = Mock()
        expected_interaction = Interaction(id=1, user_id=1, book_id=42, rating=5)
        mock_interactions_repo.insert_new_interaction.return_value = (
            expected_interaction
        )

        service = InteractionsService(mock_interactions_repo, mock_cache_repo)
        result = service.register_interaction(user_id=1, book_id=42, rating=5)

        assert result == expected_interaction
        mock_interactions_repo.insert_new_interaction.assert_called_once_with(
            user_id=1, book_id=42, rating=5
        )
        mock_cache_repo.delete_user_recommendation.assert_called_once_with(1)

    def test_register_interaction_failure_raises_exception(self):
        mock_interactions_repo = Mock()
        mock_cache_repo = Mock()
        mock_interactions_repo.insert_new_interaction.return_value = None

        service = InteractionsService(mock_interactions_repo, mock_cache_repo)

        with pytest.raises(InteractionError):
            service.register_interaction(user_id=1, book_id=42, rating=5)

        mock_interactions_repo.insert_new_interaction.assert_called_once()
        mock_cache_repo.delete_user_recommendation.assert_not_called()


class TestRecommendationService:
    def test_get_recommendations_from_cache(self):
        mock_cache_repo = Mock()
        mock_client = Mock()
        cached_books = [Book(book_id=1), Book(book_id=2)]
        mock_cache_repo.try_get_user_recommendation.return_value = cached_books

        service = RecommendationService(mock_cache_repo, mock_client)
        result = service.get_recommendations(user_id=1)

        assert result.user_id == 1
        assert result.books == cached_books
        assert result.source == "cache"
        mock_cache_repo.try_get_user_recommendation.assert_called_once()
        mock_client.get_user_recommendations.assert_not_called()

    def test_get_recommendations_from_client(self):
        mock_cache_repo = Mock()
        mock_client = Mock()
        mock_cache_repo.try_get_user_recommendation.return_value = None
        mock_client.get_user_recommendations.return_value = [1, 2, 3]

        service = RecommendationService(mock_cache_repo, mock_client)
        result = service.get_recommendations(user_id=1)

        assert result.user_id == 1
        assert len(result.books) == 3
        assert result.source == "computed"
        mock_cache_repo.try_get_user_recommendation.assert_called_once()
        mock_client.get_user_recommendations.assert_called_once()
        mock_cache_repo.set_user_recommendation.assert_called_once()

    def test_get_recommendations_empty_list(self):
        mock_cache_repo = Mock()
        mock_client = Mock()
        mock_cache_repo.try_get_user_recommendation.return_value = None
        mock_client.get_user_recommendations.return_value = []

        service = RecommendationService(mock_cache_repo, mock_client)
        result = service.get_recommendations(user_id=1)

        assert result.user_id == 1
        assert result.books == []
        assert result.source == "computed"

    def test_get_recommendations_client_raises_exception(self):
        mock_cache_repo = Mock()
        mock_client = Mock()
        mock_cache_repo.try_get_user_recommendation.return_value = None
        mock_client.get_user_recommendations.side_effect = Exception(
            "Service unavailable"
        )

        service = RecommendationService(mock_cache_repo, mock_client)

        with pytest.raises(Exception, match="Service unavailable"):
            service.get_recommendations(user_id=1)

        mock_cache_repo.set_user_recommendation.assert_not_called()
