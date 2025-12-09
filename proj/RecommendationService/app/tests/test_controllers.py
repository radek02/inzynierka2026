def test_get_user_recommendations_success(client, mock_orchestrator):
    response = client.get("/api/v1/Recommendations/user-recommendations/1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "recommended_books": [10, 20, 30]}
    mock_orchestrator.get_user_recommendation.assert_called_once_with(user_id=1)


def test_get_user_recommendations_service_error(client, mock_orchestrator):
    mock_orchestrator.get_user_recommendation.side_effect = Exception("Service error")
    response = client.get("/api/v1/Recommendations/user-recommendations/1")
    assert response.status_code == 500
