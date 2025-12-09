import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from unittest.mock import Mock

import pytest
from app.api.dependencies import get_interactions_service, get_recommendation_service
from app.main import app
from app.models import Interaction, Recommendation
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def mock_interactions_service():
    mock = Mock()
    mock.register_interaction.return_value = Interaction(
        id=1, user_id=1, book_id=2, rating=3
    )
    app.dependency_overrides[get_interactions_service] = lambda: mock
    return mock


@pytest.fixture
def mock_recommendation_service():
    mock = Mock()
    mock.get_recommendations.return_value = Recommendation(
        user_id=1, books=[], source="cache"
    )
    app.dependency_overrides[get_recommendation_service] = lambda: mock
    return mock
