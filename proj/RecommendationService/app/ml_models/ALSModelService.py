from app.models import Interaction
from typing import List
from .interfaces import IMFModelService

class ALSModelService(IMFModelService):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_model(self):
        pass

    def recompute_user_embeddings(self, interactions: List[Interaction]):
        pass