import numpy as np
import pandas as pd
from interfaces import IDataLoader
from config import AppConfig
from types import Dict

ORIGINAL_USER_ID_COLUMN_NAME = "user_id"
MAPPED_USER_ID_COLUMN_NAME = "user"
ORIGINAL_BOOK_ID_COLUMN_NAME = "book_id"
MAPPED_BOOK_ID_COLUMN_NAME = "book"

class LocalFileSystemLoader(IDataLoader):
    def __init__(self, settings: AppConfig):
        self.settings = settings

    def _create_map_dict(self, parquet_path: str, mapped_id_col_name: str, original_id_col_name: str) -> Dict[int, int]:
        df = pd.read_parquet(parquet_path)
        return dict(zip(df[mapped_id_col_name], df[original_id_col_name]))

    def load_data(self):
        return super().load_data() 