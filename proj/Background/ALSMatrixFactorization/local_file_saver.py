from interfaces import IFileSaver
from config import AppConfig
import implicit
import pandas as pd
import numpy as np
import os
import random
import string

class LocalFileSaver(IFileSaver):
    def __init__(self, config: AppConfig):
        characters = string.ascii_letters + string.digits 
        self.random_key = ''.join(random.choices(characters, k=3))
        
        os.makedirs(config.file_saving_dir, exist_ok=True)
        self.config = config

 
    def save_mappings_as_parquet(self, user_id_map: pd.DataFrame, book_id_map: pd.DataFrame):
        user_id_map.to_parquet(f"{self.config.file_saving_dir}/user_id_map_{self.random_key}.parquet")
        book_id_map.to_parquet(f"{self.config.file_saving_dir}/book_id_map_{self.random_key}.parquet")
    
    def save_embeddings_as_npy(self, model: implicit.als.AlternatingLeastSquares):
        np.save(f"{self.config.file_saving_dir}/user_embeddings_{self.config.collection_dim}d_{self.random_key}.npy", model.user_factors)
        np.save(f"{self.config.file_saving_dir}/book_embeddings_{self.config.collection_dim}d_{self.random_key}.npy", model.item_factors)