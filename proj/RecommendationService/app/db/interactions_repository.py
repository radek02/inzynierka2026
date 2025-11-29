from .interfaces import IInteractionsRepository
from psycopg2.extensions import connection
from typing import List
from app.models import Interaction

class InteractionsRepository(IInteractionsRepository):
    def __init__(self, db: connection):
        self.db = db

    def get_user_interactions(self, user_id: int) -> List[Interaction]:
        querry = """
            SELECT user_id, book_id, rating
            FROM interactions
            WHERE user_id = %s;
        """

        interactions: List[Interaction] = []

        with self.db.cursor as cur:
            cur.execute(querry, (user_id))

            rows = cur.fetchall()
            for row in rows:
                user_id_val, book_id_val, rating_val = row
                interaction = Interaction(
                    user_id=user_id_val,
                    book_id=book_id_val,
                    rating=rating_val
                )  
                interactions.append(interaction)
        
        return interactions
    