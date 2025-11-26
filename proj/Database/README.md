# Database Module

PostgreSQL database for storing user-book interactions.

**Note:** All commands assume you're running from the `proj/` directory.

## Setup

### Build Docker image
```bash
docker build -t my-postgres Database/
```

### Load .env and run
```bash
docker run -d --name postgres-db \
  --env-file Database/.env \
  -p 5432:5432 \
  my-postgres
```

### Start interactive session
```bash
docker exec -it postgres-db psql -U postgres
```

### Useful commands
```bash
# Check if container is running
docker ps

# Stop the container
docker stop postgres-db

# Start existing container
docker start postgres-db

# Remove container (to rebuild)
docker rm postgres-db

# View logs
docker logs postgres-db
```

## Schema

The database contains:
- `user_book_interactions` table - stores user ratings for books
- Indexes on `user_id`, `book_id`, and `created_at`
- `interaction_stats` view - provides quick statistics

See `schema.sql` for full schema definition.

## Loading Data
This chapter is required to first database initialization which should be to load data into a database.
### Install Python dependencies
```bash
cd Database
pip install -r requirements.txt
```

### Load all interactions from CSV file
```bash
# From proj/Database/ directory
# Uses default path: /Users/rmaksymiuk/MINI/inzynierka/data/goodreads_interactions.csv
python load_interactions.py

# Or specify a custom path
python load_interactions.py /path/to/your/interactions.csv
```

### Expected CSV format
The CSV file should have the following columns:
- `user_id` (integer)
- `book_id` (integer)
- `rating` (integer, 0-5 scale)

Additional columns in the CSV (like `is_read`, `is_reviewed`) will be ignored.

### View statistics
After loading, the script will display statistics. You can also query them manually:
```sql
SELECT * FROM interaction_stats;
```

## Example Queries

```sql
-- Get all interactions for a specific user
SELECT * FROM user_book_interactions WHERE user_id = 123;

-- Get average rating for a specific book
SELECT book_id, AVG(rating) as avg_rating, COUNT(*) as rating_count
FROM user_book_interactions
WHERE book_id = 456
GROUP BY book_id;

-- Find most active users
SELECT user_id, COUNT(*) as interaction_count
FROM user_book_interactions
GROUP BY user_id
ORDER BY interaction_count DESC
LIMIT 10;
```