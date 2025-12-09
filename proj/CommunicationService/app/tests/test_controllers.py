def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_post_interactions(client, mock_interactions_service):
    response = client.post(
        "/api/v1/interactions",
        json={
            "user_id": 1,
            "book_id": 2,
            "rating": 3,
        },
    )
    assert response.status_code == 201
    mock_interactions_service.register_interaction.assert_called_once_with(
        user_id=1, book_id=2, rating=3
    )


def test_get_recommendation(client, mock_recommendation_service):
    response = client.get(
        "/api/v1/recommendations?user_id=1",
    )
    assert response.status_code == 200
    mock_recommendation_service.get_recommendations.assert_called_once_with(
        user_id=1,
    )
