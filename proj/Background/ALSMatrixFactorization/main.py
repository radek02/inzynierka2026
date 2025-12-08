from config import settings
from local_file_saver import LocalFileSaver
from local_model_saver import LocalModelSaver
from als_matrix_factorization import ALSMatrixFactorization
from interactions_service import InteractionsService
from local_interactions_loader import LocalInteractionsLoader

def main():
    local_interactions_loader = LocalInteractionsLoader(config=settings)
    interactions_service = InteractionsService(interactions_loader=local_interactions_loader)
    local_model_saver = LocalModelSaver(config=settings)
    local_file_saver = LocalFileSaver(config=settings)
    als_matrix_factorization = ALSMatrixFactorization(interactions_service=interactions_service, file_saver=local_file_saver,
                                                      model_saver=local_model_saver, config=settings)
    als_matrix_factorization.do_factorization()

if __name__ == '__main__':
    main()