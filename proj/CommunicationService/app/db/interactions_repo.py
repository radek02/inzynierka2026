from psycopg2.extensions import connection

from app.models import Interaction


class InteractionsRepository:
    def __init__(self, db: connection):
        self.db = db

    def insert_new_interaction(self, user_id: int, book_id: int, rating: int) -> Interaction | None:
        query = """
            INSERT INTO user_book_interactions (user_id, book_id, rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, book_id) DO UPDATE
            SET rating = EXCLUDED.rating, created_at = CURRENT_TIMESTAMP
            RETURNING id, user_id, book_id, rating;
        """
        try:
            with self.db.cursor() as cur:
                cur.execute(query, (user_id, book_id, rating))
                result = cur.fetchone()
                self.db.commit()
                if result:
                    return Interaction(
                        id=result[0],
                        user_id=result[1],
                        book_id=result[2],
                        rating=result[3],
                    )
                return None
        except Exception:
            self.db.rollback()
            raise