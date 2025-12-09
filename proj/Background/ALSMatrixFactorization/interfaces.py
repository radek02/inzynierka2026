from abc import ABC, abstractmethod
import pandas as pd
import implicit

class IInteractionsLoader(ABC):
    @abstractmethod
    def load_interactions(self) -> pd.DataFrame:
        pass

class IFileSaver(ABC):
    @abstractmethod
    def save_mappings_as_parquet(self, user_id_map: pd.DataFrame, book_id_map: pd.DataFrame):
        pass
    
    @abstractmethod
    def save_embeddings_as_npy(self, model: implicit.als.AlternatingLeastSquares):
        pass

class IModelSaver(ABC):
    @abstractmethod
    def save_model_as_pkl(self, model: implicit.als.AlternatingLeastSquares):
        pass