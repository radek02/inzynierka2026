from abc import ABC, abstractmethod
from app.models import Interaction
from typing import List

class IMFModelService(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def recompute_user_embeddings(self, interactions: List[Interaction]):
        pass

class IModelLoader(ABC):
    @abstractmethod
    def load_mf_model(self):
        pass