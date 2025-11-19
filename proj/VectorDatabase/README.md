# Overview
Data is stored in folder qdrant_data, this folder is added to .gitignor

Connection from Python, authentication do not needed:

```
from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://localhost:6333",
)
```
# Run
To run qdrant for Windows call:
```
powershell -ExecutionPolicy Bypass -File .\windows-run-qdrant.ps1
```

To run qdrant for Mac call:
```
TODO: I don't now what
```
# Helthcheck
To check helth, you can write in your browser:
```
http://localhost:6333/healthz
```