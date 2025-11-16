# Install dependencies
`pip install -r requirements.txt`

# Run locally
`python main` will expose endpoints at `localhost:8001`, view Swagger at `localhost:8001/docs`

# Build Docker image
```
docker build -t recommendation-service .
```
Execute the above command insdie `RecommendationService` directory.

# Run Docker image
```
docker run -d -p 8001:8000 recommendation-service
```
The endpoints will be exposed at `localhost:8001`, the same as if run locally.
