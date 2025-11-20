from config import settings
from data_loader import LocalFileSystemLoader
from qdrant_repository import QdrantRepository

def main():
    loader = LocalFileSystemLoader(settings=settings)
    vector_repository = QdrantRepository(url=settings.qdrant_url)

    print(f"Loading data from {settings.user_embeddings_path} and {settings.book_embeddings_path}...")
    users_data, books_data = loader.load_embeddings()
    user_id_map, book_id_map = loader.load_id_maps()

    print("Initializing vector database collections...")
    vector_repository.recreate_collection(dim=settings.collection_dim)

    print("Uploading books...")
    vector_repository.upload_vectors("books", books_data, book_id_map, settings.batch_size)

    print("Uploading users...")
    vector_repository.upload_vectors("users", users_data, user_id_map, settings.batch_size)

    print("Creating indexing...")
    vector_repository.create_indexing("books")
    vector_repository.create_indexing("users")

    print("Succeded")

if __name__ == '__main__':
    main()