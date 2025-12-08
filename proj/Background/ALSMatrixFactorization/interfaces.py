from abc import ABC, abstractmethod
import pandas as pd

class IInteractionsLoader(ABC):
    @abstractmethod
    def load_interactions(self) -> pd.DataFrame:
        pass