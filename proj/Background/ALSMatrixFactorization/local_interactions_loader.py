from interfaces import IInteractionsLoader
from config import AppConfig
import pandas as pd

class LocalInteractionsLoader(IInteractionsLoader):
    def __init__(self, config: AppConfig):
        self.config = config

    def load_interactions(self) -> pd.DataFrame:
        df = pd.read_csv(self.config.interactions_path)
        return df