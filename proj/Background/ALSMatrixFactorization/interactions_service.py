from interfaces import IInteractionsLoader
import pandas as pd
from typing import Tuple

class InteractionsService:
    def __init__(self, interactions_loader: IInteractionsLoader):
        self.interactions_loader = interactions_loader

    def get_interactions(self) -> Tuple[pd.DataFrame, int, int]:
        df = self.interactions_loader.load_interactions()

        df["user"] = df["user_id"].astype("category").cat.codes
        df["book"] = df["book_id"].astype("category").cat.codes

        num_users = df["user"].nunique()
        num_items = df["book"].nunique()

        print(f"Users: {num_users:,}  |  Books: {num_items:,}  |  Interactions: {len(df):,}")

        return df, num_users, num_items