"""Script to load user-book interactions from CSV into PostgreSQL using COPY."""

import os
import sys
import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def confirm_db_action(action_description):
    """
    Display database connection details and ask for confirmation before proceeding.

    Parameters:
    - action_description: Description of the action to be performed

    Returns:
    - True if user confirms, False otherwise
    """
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "mydb")
    user = os.getenv("POSTGRES_USER", "postgres")

    print("\n" + "=" * 60)
    print("DATABASE CONNECTION DETAILS")
    print("=" * 60)
    print(f"Host:     {host}")
    print(f"Port:     {port}")
    print(f"Database: {database}")
    print(f"User:     {user}")
    print("=" * 60)
    print(f"\nAction: {action_description}")
    print("=" * 60)

    response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    return response in ["yes", "y"]


def get_db_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "mydb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "pass"),
    )


def create_schema(conn):
    """Create the database schema if it doesn't exist."""
    schema_file = Path(__file__).parent / "schema.sql"

    with open(schema_file, "r") as f:
        schema_sql = f.read()

    with conn.cursor() as cur:
        cur.execute(schema_sql)

    conn.commit()
    print("✓ Schema created successfully")


def bulk_load_with_copy(conn, csv_path):
    """
    Load CSV directly using COPY command.

    Parameters:
    - conn: PostgreSQL connection
    - csv_path: Path to CSV file with columns: user_id, book_id, rating
    """
    print(f"\nLoading from: {csv_path}")
    start_time = time.time()

    with conn.cursor() as cur:
        # Step 1: Create temporary table without constraints (faster loading)
        print("Creating temporary staging table...")
        cur.execute("""
            CREATE TEMP TABLE temp_interactions (
                user_id INTEGER,
                book_id INTEGER,
                is_read SMALLINT,
                rating SMALLINT,
                is_reviewed SMALLINT
            );
        """)

        # Step 2: COPY data into temp table
        print("Copying data from CSV (this is fast)...")
        copy_start = time.time()

        with open(csv_path, 'r') as f:
            # Skip header row if present
            next(f)

            # Load all columns from CSV
            cur.copy_expert(
                "COPY temp_interactions (user_id, book_id, is_read, rating, is_reviewed) FROM STDIN WITH CSV",
                f
            )

        copy_time = time.time() - copy_start

        # Get count from temp table
        cur.execute("SELECT COUNT(*) FROM temp_interactions")
        temp_count = cur.fetchone()[0]
        print(f"✓ Copied {temp_count:,} rows to staging table in {copy_time:.1f}s")

        # Step 3: Insert from temp table to real table
        # This preserves all schema constraints (SERIAL id, DEFAULT created_at, etc.)
        print("Inserting into main table (preserving schema)...")
        insert_start = time.time()

        cur.execute("""
            INSERT INTO user_book_interactions (user_id, book_id, rating)
            SELECT user_id, book_id, rating
            FROM temp_interactions
            ON CONFLICT (user_id, book_id)
            DO UPDATE SET
                rating = EXCLUDED.rating,
                created_at = CURRENT_TIMESTAMP;
        """)

        insert_time = time.time() - insert_start
        rows_inserted = cur.rowcount

        conn.commit()

        total_time = time.time() - start_time

        print(f"✓ Inserted {rows_inserted:,} interactions in {insert_time:.1f}s")
        print(f"✓ Total time: {total_time:.1f}s")
        print(f"  Average: {rows_inserted/total_time:,.0f} rows/second")


def display_stats(conn):
    """Display statistics about the loaded data."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM interaction_stats")
        stats = cur.fetchone()

        if stats:
            print("\n" + "=" * 60)
            print("DATABASE STATISTICS")
            print("=" * 60)
            print(f"Total interactions:     {stats[0]:,}")
            print(f"Unique users:           {stats[1]:,}")
            print(f"Unique books:           {stats[2]:,}")
            print(f"Average rating:         {stats[3]:.2f}")
            print(f"Earliest interaction:   {stats[4]}")
            print(f"Latest interaction:     {stats[5]}")
            print("=" * 60)


def main():
    # Check if file path is provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default path to CSV file
        file_path = "/Users/rmaksymiuk/MINI/inzynierka/data/goodreads_interactions.csv"
        print(f"Using default path: {file_path}")

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        print(f"Usage: python {sys.argv[0]} <path_to_csv>")
        sys.exit(1)

    # Get file size for display
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    try:
        # Ask for confirmation before proceeding
        action_description = (
            f"Bulk load interactions from {os.path.basename(file_path)} "
            f"({file_size_mb:.1f} MB) using optimized COPY method"
        )
        if not confirm_db_action(action_description):
            print("\n✗ Operation cancelled by user")
            sys.exit(0)

        # Connect to database
        print("\nConnecting to PostgreSQL...")
        conn = get_db_connection()
        print("✓ Connected successfully")

        # Create schema
        print("\nEnsuring schema exists...")
        create_schema(conn)

        # Bulk load data using COPY
        bulk_load_with_copy(conn, file_path)

        # Display statistics
        display_stats(conn)

        conn.close()
        print("\n✓ All done!")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
