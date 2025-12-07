from .interfaces import IModelLoader
from app.core import AppConfig
import pickle
import os

class LocalModelLoader(IModelLoader):
    def __init__(self, config: AppConfig):
        self.config = config

    def load_mf_model(self):
        if os.path.exists(self.config.mf_model_path):
            with open(self.config.mf_model_path, "rb") as f:
                return pickle.load(f)
        else:
            return None
