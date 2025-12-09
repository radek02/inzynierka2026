from app.models import UserRecommendationResponse
from app.services import ICandidateGeneratorService, IRankerService, IReRankerService


class UserRecommendationOrchestrator:
    def __init__(
        self,
        candidate_generator: ICandidateGeneratorService,
        ranker: IRankerService,
        reranker: IReRankerService,
    ):
        self.candidate_generator = candidate_generator
        self.ranker = ranker
        self.reranker = reranker

    def get_user_recommendation(self, user_id):
        candidates = self.candidate_generator.generate_candidates(user_id=user_id)
        ranked_books = self.ranker.rank_candidates([0, 0], candidates=candidates)
        final_recommendation = self.reranker.rerank(ranked_books)

        result = UserRecommendationResponse(
            user_id=user_id, recommended_books=final_recommendation
        )

        return result
