# Build
`docker build -t my-postgres Database/`

# Load .env and run
```
docker run -d --name postgres-db \
  --env-file .env.example \
  -p 5432:5432 \
  my-postgres
```

# Start interactive session
`docker exec -it postgres-db psql -U postgres`