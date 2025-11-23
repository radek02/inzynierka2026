"""
Script to load 10% of user-book interactions from CSV file into PostgreSQL.
Similar pattern to EDA.ipynb for loading books data.
"""

import os
import sys
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
from pathlib import Path

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

    print("\n" + "="*60)
    print("DATABASE CONNECTION DETAILS")
    print("="*60)
    print(f"Host:     {host}")
    print(f"Port:     {port}")
    print(f"Database: {database}")
    print(f"User:     {user}")
    print("="*60)
    print(f"\nAction: {action_description}")
    print("="*60)

    response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def get_db_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "mydb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "pass")
    )

def load_interactions(file_path):
    """
    Load all interactions from CSV file.

    Parameters:
    - file_path: path to the .csv file

    Returns:
    - pandas DataFrame with all data
    """
    print(f"Loading interactions from: {file_path}")

    # Read entire CSV file
    df = pd.read_csv(file_path)

    print(f"Loaded {len(df):,} interactions")

    return df

def create_schema(conn):
    """Create the database schema if it doesn't exist."""
    schema_file = Path(__file__).parent / "schema.sql"

    with open(schema_file, 'r') as f:
        schema_sql = f.read()

    with conn.cursor() as cur:
        cur.execute(schema_sql)

    conn.commit()
    print("Schema created successfully")

def insert_interactions(conn, df):
    """
    Insert interactions into the database using batch insert for efficiency.

    Parameters:
    - conn: PostgreSQL connection
    - df: DataFrame with columns: user_id, book_id, rating
    """
    # Show available columns for debugging
    print(f"\nAvailable columns in data: {list(df.columns)}")
    print(f"First row sample: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")

    # Validate required columns
    required_columns = ['user_id', 'book_id', 'rating']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}. Available columns: {list(df.columns)}")

    # Clean data
    df = df[required_columns].copy()
    df = df.dropna()  # Remove rows with missing values

    # Convert to appropriate types
    # CSV already has numeric IDs
    df['user_id'] = df['user_id'].astype(int)
    df['book_id'] = df['book_id'].astype(int)
    df['rating'] = df['rating'].astype(int)  # rating is an integer 0-5

    # Validate rating range
    if not df['rating'].between(0, 5).all():
        print("Warning: Some ratings are outside the 0-5 range. Clipping values...")
        df['rating'] = df['rating'].clip(0, 5)

    print(f"\nPreparing to insert {len(df):,} interactions...")
    print(f"User IDs range: {df['user_id'].min()} - {df['user_id'].max()}")
    print(f"Book IDs range: {df['book_id'].min()} - {df['book_id'].max()}")
    print(f"Rating statistics:\n{df['rating'].describe()}")

    # Prepare data for insertion
    records = df.to_records(index=False)
    data = [(int(r.user_id), int(r.book_id), float(r.rating)) for r in records]

    # Insert using batch for better performance
    insert_query = """
        INSERT INTO user_book_interactions (user_id, book_id, rating)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, book_id) DO UPDATE
        SET rating = EXCLUDED.rating,
            created_at = CURRENT_TIMESTAMP;
    """

    with conn.cursor() as cur:
        execute_batch(cur, insert_query, data, page_size=1000)

    conn.commit()
    print(f"✓ Successfully inserted {len(df):,} interactions")

def display_stats(conn):
    """Display statistics about the inserted data."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM interaction_stats")
        stats = cur.fetchone()

        if stats:
            print("\n" + "="*60)
            print("DATABASE STATISTICS")
            print("="*60)
            print(f"Total interactions:     {stats[0]:,}")
            print(f"Unique users:           {stats[1]:,}")
            print(f"Unique books:           {stats[2]:,}")
            print(f"Average rating:         {stats[3]:.2f}")
            print(f"Earliest interaction:   {stats[4]}")
            print(f"Latest interaction:     {stats[5]}")
            print("="*60)

def main():
    """Main execution function."""
    # Check if file path is provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default path to CSV file
        file_path = "/Users/rmaksymiuk/MINI/inzynierka/data/goodreads_interactions.csv"
        print(f"Using default path: {file_path}")

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    try:
        # Load all data from CSV file
        df = load_interactions(file_path)

        # Ask for confirmation before proceeding with database operations
        action_description = f"Load {len(df):,} interactions from {os.path.basename(file_path)}"
        if not confirm_db_action(action_description):
            print("\n✗ Operation cancelled by user")
            sys.exit(0)

        # Connect to database
        print("\nConnecting to PostgreSQL...")
        conn = get_db_connection()
        print("✓ Connected successfully")

        # Create schema
        print("\nCreating schema...")
        create_schema(conn)

        # Insert data
        print("\nInserting interactions...")
        insert_interactions(conn, df)

        # Display statistics
        display_stats(conn)

        conn.close()
        print("\n✓ All done!")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
