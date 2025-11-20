from abc import ABC, abstractmethod
from typing import List, Dict,  Any
import numpy as np

class IDataLoader(ABC):
    @abstractmethod
    def load_embeddings(self) -> tuple[np.ndarray, np.ndarray]:
        """Returns a tuple of (user_embeddings, book_embeddings). 
           Data structure: {id: vector}
        """
        pass

    @abstractmethod
    def load_id_maps(self) -> tuple[Dict[int, int], Dict[int, int]]:
        """Returns a tuple of (user_id_map, book_id_map). 
           Data structure: {mapped_id: original_id}
        """
        pass

class IVectorRepository(ABC):
    @abstractmethod
    def recreate_collection(self, dim: int) -> None:
        pass

    @abstractmethod
    def upload_vectors(self, collection_name: str, data: Dict[int, List[float]], id_map: Dict[int, int], batch_size: int) -> None:
        pass

    @abstractmethod
    def create_indexing(self, collection_name: str) -> None:
        pass 