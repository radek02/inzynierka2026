# Overview
Vector database model used to store all users embeddings and books embeddings allowing fast similarity search.



# Run via docker
After running qdrant will be exposed in adress http://localhost:6333

**Note: docker container will store all data saved in qdrant, and this data will be stored in qdrant_data/ folder (which will be created locally after first run of the container)**

## To run qdrant for Windows call:
```
powershell -ExecutionPolicy Bypass -File .\windows-run-qdrant.ps1
```

## To run qdrant for Mac call:
```
TODO
```
## Helthcheck
To check helth, you can write in your browser:
```
http://localhost:6333/healthz
```