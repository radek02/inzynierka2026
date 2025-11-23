FROM postgres:15-alpine

# Copy schema to be executed on container startup
COPY schema.sql /docker-entrypoint-initdb.d/

# Environment variables (override with --env-file or -e)
ENV POSTGRES_DB=interactions
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres