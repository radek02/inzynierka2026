from .interfaces import IReRankerService

class ReRankerService(IReRankerService):
    def __init__(self):
        pass

    def rerank(self, book_ids: List[int]) -> List[int]:
        return book_ids