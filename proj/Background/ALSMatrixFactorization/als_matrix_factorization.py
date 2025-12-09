import implicit
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from interactions_service import InteractionsService
import os
from interfaces import IFileSaver, IModelSaver
from config import AppConfig

class ALSMatrixFactorization:
    def __init__(self, interactions_service: InteractionsService,
                 file_saver: IFileSaver,
                 model_saver: IModelSaver,
                 config: AppConfig):
        self.interactions_service = interactions_service
        self.file_saver = file_saver
        self.model_saver = model_saver
        self.embedding_dim = config.collection_dim
        self.config = config

    def do_factorization(self):
        df, num_users, num_items = self.interactions_service.get_interactions()

        ratings_coo = coo_matrix(
            (df["rating"].astype(float), (df["user"], df["book"])), shape=(num_users, num_items)
        )

        ratings_csr = ratings_coo.tocsr()

        # Train ALS model
        model = implicit.als.AlternatingLeastSquares(
            factors=self.embedding_dim, regularization=self.config.als_regularization, iterations=self.config.als_epochs, use_gpu=False
        )
        os.environ["OPENBLAS_NUM_THREADS"] = "1"

        print("Training ALS...")
        model.fit(ratings_csr)
        print("Training finished.")

        self._save_mappings(df=df)
        self._save_embeddings(model=model)
        self._save_model(model=model)

    def _save_mappings(self, df: pd.DataFrame):
        user_id_map = df[["user", "user_id"]].drop_duplicates().sort_values("user")
        book_id_map = df[["book", "book_id"]].drop_duplicates().sort_values("book")
        self.file_saver.save_mappings_as_parquet(user_id_map=user_id_map, book_id_map=book_id_map)
        print("Mappings saved")

    def _save_embeddings(self, model: implicit.als.AlternatingLeastSquares):
        self.file_saver.save_embeddings_as_npy(model=model)
        print("Embeddings saved")

    def _save_model(self, model: implicit.als.AlternatingLeastSquares):
        self.model_saver.save_model_as_pkl(model=model)
        print("Model saved")