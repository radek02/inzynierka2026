# Book Recommendation System - Project Modules

This directory contains all the service modules for the book recommendation system.


## Project Structure

```
proj/
├── Database/                   # PostgreSQL database module
├── CommunicationService/       # API gateway service
├── RecommendationService/      # ML recommendation engine
├── VectorDatabase/             # Vector database for embeddings
└── Cache/                      # Redis cache module
```

## Setup

**Python Version:** This project uses Python 3.14 (both locally and in Docker).

## Module Documentation

See individual module READMEs for specific instructions:
- [Database](Database/README.md) - Interactions storage, PostgreSQL setup and data loading
- [CommunicationService](CommunicationService/README.md) - API gateway
- [RecommendationService](RecommendationService/README.md) - ML service
- [VectorDatabase](VectorDatabase/README.md) - Embeddings storage
- [Background](Background/README.md) - Background scripts


## Updating Dependencies

If you add new dependencies to a specific module:

1. Add to the module's `requirements.txt`
2. Reinstall from module's directory:
```bash
pip install -r Database/requirements.txt
```
