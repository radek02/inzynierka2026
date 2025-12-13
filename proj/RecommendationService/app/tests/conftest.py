import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from unittest.mock import Mock

import pytest
from app.core.dependency_container import get_user_recommendation_orchestrator
from app.main import app
from app.models import UserRecommendationResponse
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def mock_orchestrator():
    mock = Mock()
    mock.get_user_recommendation.return_value = UserRecommendationResponse(
        user_id=1, recommended_books=[10, 20, 30]
    )
    app.dependency_overrides[get_user_recommendation_orchestrator] = lambda: mock
    return mock
