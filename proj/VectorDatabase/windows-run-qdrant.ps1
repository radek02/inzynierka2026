$storagePath = "qdrant_data"
if (!(Test-Path $storagePath)) {
    New-Item -ItemType Directory -Path $storagePath | Out-Null
}

docker build -t my-qdrant .

try {
    docker stop qdrant | Out-Null
    docker rm qdrant | Out-Null
}
catch {
}
try {
    docker run -d `
        --name qdrant `
        -p 6333:6333 `
        -p 6334:6334 `
        -v "$PWD\qdrant_data:/qdrant/storage" `
        my-qdrant

    Write-Host "Qdrant is running at http://localhost:6333"
}
catch {
    Write-Host "Failed"
}