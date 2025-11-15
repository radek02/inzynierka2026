mkdir -p qdrant_data

docker build -t my-qdrant .

docker stop qdrant 2>/dev/null
docker rm qdrant 2>/dev/null

docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_data:/qdrant/storage \
  my-qdrant

echo "Qdrant running at http://localhost:6333"