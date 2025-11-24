from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from typing import List

class InteractionsRepository:
    def __init__(self, db: connection):
        self.db = db

    def insert_new_interaction(self, user_id: int, book_id: int, rating: int) -> bool:
        query = """
            INSERT INTO user_book_interactions (user_id, book_id, rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, book_id) DO UPDATE
            SET rating = EXCLUDED.rating, created_at = CURRENT_TIMESTAMP
            RETURNING id;
        """
        try:
            with self.db.cursor() as cur:
                cur.execute(query, (user_id, book_id, rating))
                result = cur.fetchone()
                self.db.commit()
                return result is not None
        except Exception as e:
            self.db.rollback()
            raise