$storagePath = "qdrant_data"
if (!(Test-Path $storagePath)) {
    New-Item -ItemType Directory -Path $storagePath | Out-Null
}

docker build -t my-qdrant .

docker stop qdrant -ErrorAction SilentlyContinue
docker rm qdrant -ErrorAction SilentlyContinue

docker run -d `
    --name qdrant `
    -p 6333:6333 `
    -p 6334:6334 `
    -v "$PWD\qdrant_data:/qdrant/storage" `
    my-qdrant

Write-Host "Qdrant is running at http://localhost:6333"
