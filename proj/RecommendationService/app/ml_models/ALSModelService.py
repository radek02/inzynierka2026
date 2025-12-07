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
        if not self.model:
            raise RuntimeError("Model is not loaded.")
        
        book_als_ids = [i.mf_id for i in interactions]
        ratings = [i.rating for i in interactions]

        user_sparse = sparse.csr_matrix(
            (ratings, ([0] * len(book_als_ids), book_als_ids)),
            shape=(1, self.model.item_factors.shape[0]) 
        ) 

        new_vector = self.model.recalculate_user(0, user_sparse)

        return new_vector