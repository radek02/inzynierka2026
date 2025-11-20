from abc import ABC, abstractmethod
from typing import List, Dict,  Any

class IDataLoader(ABC):
    @abstractmethod
    def load_data(self) -> tuple[Dict[int, List[float]], Dict[int, List[float]]]:
        """Returns a tuple of (user_embeddings, book_embeddings). 
           Data structure: {id: vector}
        """
        pass

class IVectorRepository(ABC):
    @abstractmethod
    def recreate_collection(self, dim: int) -> None:
        pass

    @abstractmethod
    def upload_vectors(self, collection_name: str, data: Dict[int, List[float]], batch_size: int) -> None:
        pass

    @abstractmethod
    def create_indexing(self, collection_name: str) -> None:
        pass 