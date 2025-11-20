from config import settings
from data_loader import LocalFileSystemLoader
from qdrant_repository import QdrantRepository

def main():
    loader = LocalFileSystemLoader(settings=settings)
    vector_repository = QdrantRepository(url=settings.qdrant_url)

    print(f"Loading data from {settings.user_embeddings_path} and {settings.book_embeddings_path}...")
    users_data, books_data = loader.load_data() 

    print("Initializing vector database collections...")
    vector_repository.recreate_collections(dim=settings.collection_dim)

    print("Uploading books...")
    vector_repository.upload_vectors("books", books_data, settings.batch_size)

    print("Uploading users...")
    vector_repository.upload_vectors("users", users_data, settings.batch_size)

    print("Creating indexing...")
    vector_repository.optimize("books")
    vector_repository.optimize("users")

    print("Succeded")

if __name__ == '__main__':
    main()