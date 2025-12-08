from interfaces import IModelSaver
from config import AppConfig
import implicit
import pickle
import string
import random
import os

class LocalModelSaver(IModelSaver):
    def __init__(self, config: AppConfig):
        characters = string.ascii_letters + string.digits 
        self.random_key = ''.join(random.choices(characters, k=3))
        
        os.makedirs(config.model_saving_dir, exist_ok=True)
        self.config = config

    def save_model_as_pkl(self, model: implicit.als.AlternatingLeastSquares):
        with open(f"{self.config.model_saving_dir}/als_model_{self.random_key}.pkl", "wb") as f:
            pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)