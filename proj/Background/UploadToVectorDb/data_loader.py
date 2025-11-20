import numpy as np
import pandas as pd
from interfaces import IDataLoader
from config import AppConfig

ORIGINAL_USER_ID_COLUMN_NAME = "user_id"
MAPPED_USER_ID_COLUMN_NAME = "user"
ORIGINAL_BOOK_ID_COLUMN_NAME = "book_id"
MAPPED_BOOK_ID_COLUMN_NAME = "book"

class LocalFileSystemLoader(IDataLoader):
    def __init__(self, settings: AppConfig):
        self.settings = settings        

    def load_id_maps(self):
        df_users = pd.read_parquet(self.settings.user_mapping_path)
        df_books = pd.read_parquet(self.settings.book_mapping_path)
        user_id_map = dict(zip(df_users[MAPPED_USER_ID_COLUMN_NAME], df_users[ORIGINAL_USER_ID_COLUMN_NAME]))
        book_id_map = dict(zip(df_books[MAPPED_BOOK_ID_COLUMN_NAME], df_books[ORIGINAL_BOOK_ID_COLUMN_NAME]))
        return user_id_map, book_id_map

    def load_embeddings(self):
        user_embeddings = np.load(self.settings.user_embeddings_path)
        book_embeddings = np.load(self.settings.book_embeddings_path)

        return user_embeddings, book_embeddings 