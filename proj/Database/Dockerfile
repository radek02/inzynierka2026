# Use official PostgreSQL image
FROM postgres:16-alpine

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=mydatabase

# Expose PostgreSQL port
EXPOSE 5432

# PostgreSQL data will be stored in a volume
VOLUME ["/var/lib/postgresql/data"]
