from unittest.mock import Mock

import pytest
from app.models import GeneratedCandidate, UserRecommendationResponse
from app.services import (
    CandidateGeneratorService,
    RankerService,
    ReRankerService,
    UserRecommendationOrchestrator,
)


class TestUserRecommendationOrchestrator:
    def test_get_recommendation_success(self):
        mock_candidate_generator = Mock()
        mock_ranker = Mock()
        mock_reranker = Mock()

        candidates = [
            GeneratedCandidate(book_id=1, book_embeddings=[0.1, 0.2], score=0.9),
            GeneratedCandidate(book_id=2, book_embeddings=[0.3, 0.4], score=0.8),
        ]
        mock_candidate_generator.generate_candidates.return_value = candidates
        mock_ranker.rank_candidates.return_value = [1, 2]
        mock_reranker.rerank.return_value = [1, 2]

        orchestrator = UserRecommendationOrchestrator(
            mock_candidate_generator, mock_ranker, mock_reranker
        )
        result = orchestrator.get_user_recommendation(user_id=1)

        assert result.user_id == 1
        assert result.recommended_books == [1, 2]
        mock_candidate_generator.generate_candidates.assert_called_once_with(user_id=1)

    def test_get_recommendation_no_candidates(self):
        mock_candidate_generator = Mock()
        mock_ranker = Mock()
        mock_reranker = Mock()

        mock_candidate_generator.generate_candidates.return_value = []
        mock_ranker.rank_candidates.return_value = []
        mock_reranker.rerank.return_value = []

        orchestrator = UserRecommendationOrchestrator(
            mock_candidate_generator, mock_ranker, mock_reranker
        )
        result = orchestrator.get_user_recommendation(user_id=1)

        assert result.recommended_books == []


class TestCandidateGeneratorService:
    def test_generate_candidates_success(self):
        mock_embeddings_repo = Mock()
        mock_embeddings_repo.get_user_embeddings.return_value = [0.1, 0.2, 0.3]
        mock_embeddings_repo.get_best_books.return_value = [
            GeneratedCandidate(book_id=1, book_embeddings=[0.1], score=0.9),
        ]

        service = CandidateGeneratorService(mock_embeddings_repo)
        result = service.generate_candidates(user_id=1)

        assert len(result) == 1
        assert result[0].book_id == 1
        mock_embeddings_repo.get_user_embeddings.assert_called_once_with(1)

    def test_generate_candidates_user_not_found(self):
        mock_embeddings_repo = Mock()
        mock_embeddings_repo.get_user_embeddings.side_effect = ValueError(
            "User not found"
        )

        service = CandidateGeneratorService(mock_embeddings_repo)

        with pytest.raises(ValueError):
            service.generate_candidates(user_id=999)


class TestRankerService:
    def test_rank_candidates_success(self):
        candidates = [
            GeneratedCandidate(book_id=10, book_embeddings=[0.1], score=0.9),
            GeneratedCandidate(book_id=20, book_embeddings=[0.2], score=0.8),
        ]

        service = RankerService()
        result = service.rank_candidates([0.1, 0.2], candidates)

        assert result == [10, 20]

    def test_rank_empty_candidates(self):
        service = RankerService()
        result = service.rank_candidates([0.1, 0.2], [])

        assert result == []


class TestReRankerService:
    def test_rerank_success(self):
        service = ReRankerService()
        result = service.rerank([1, 2, 3])

        assert result == [1, 2, 3]
