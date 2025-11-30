from app.models import Interaction
from typing import List
from .interfaces import IMFModelService, IModelLoader
import scipy.sparse as sparse
import implicit

class ALSModelService(IMFModelService):
    def __init__(self, model_loader: IModelLoader):
        self.model_loader = model_loader 
        self.model = None

    def load_model(self):
        self.model = self.model_loader.load_mf_model()
        if self.model is None:
            print(f"Warning: Model file not found. Embeddings update is unavailable.")
        else:
            print("MF model loaded successfully.")
            

    def recompute_user_embeddings(self, interactions: List[Interaction]) -> List[float]:
        pass