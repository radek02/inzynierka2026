# Install dependencies
`pip install -r requirements.txt`

# Run locally
`python main` will expose endpoints at `localhost:8000`, view Swagger at `localhost:8000/docs`

# Build Docker image
```
docker build -t communication-service .
```
Execute the above command insdie `CommunicationServie` directory.

# Run Docker image
```
docker run -d -p 8000:8000 communication-service
```
The endpoints will be exposed at `localhost:8000`, the same as if run locally.