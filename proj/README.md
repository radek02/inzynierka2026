# Book Recommendation System - Project Modules

This directory contains all the service modules for the book recommendation system.

**Note:** All commands assume you're running from the `proj/` directory.

## Project Structure

```
proj/
├── .venv/                      # Single virtual environment for all modules
├── requirements.txt            # Combined requirements
├── Database/                   # PostgreSQL database module
├── CommunicationService/       # API gateway service
├── RecommendationService/      # ML recommendation engine
├── VectorDatabase/             # Vector database for embeddings
└── Cache/                      # Redis cache module
```

## Setup

**Python Version:** This project uses Python 3.14 (both locally and in Docker).

### 1. Create virtual environment
```bash
# From proj/ directory
# Make sure you have Python 3.14 installed
python3.14 -m venv .venv

# Or if python3 already points to 3.14:
python3 -m venv .venv
```

### 2. Activate virtual environment
```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 3. Install all dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install dependencies for all modules at once.

### 4. Set up environment variables
Each module has its own `.env` file. Copy the example files:
```bash
cp Database/.env.example Database/.env
cp CommunicationService/.env.example CommunicationService/.env
cp RecommendationService/.env.example RecommendationService/.env
```

Then edit each `.env` file with your actual configuration.

## Module Documentation

See individual module READMEs for specific instructions:
- [Database](Database/README.md) - PostgreSQL setup and data loading
- [CommunicationService](CommunicationService/README.md) - API gateway
- [RecommendationService](RecommendationService/README.md) - ML service

## Development Workflow

```bash
# 1. Navigate to proj/
cd proj/

# 2. Activate virtual environment (if not already active)
source .venv/bin/activate

# 3. Work on any module - all dependencies are available
cd Database/
python load_interactions.py

cd ../CommunicationService/
python main.py

# etc.
```

## Quick Start

1. **Start the database:**
   ```bash
   docker build -t my-postgres Database/
   docker run -d --name postgres-db --env-file Database/.env -p 5432:5432 my-postgres
   ```

2. **Load interactions data:**
   ```bash
   cd Database
   python load_interactions.py
   cd ..
   ```

3. **Start services:**
   ```bash
   # Communication Service
   cd CommunicationService
   python main.py
   ```

## Updating Dependencies

If you add new dependencies to a specific module:

1. Add to the module's `requirements.txt`
2. Reinstall from root:
   ```bash
   # From proj/
   pip install -r requirements.txt
   ```

Or install the specific module's requirements:
```bash
pip install -r Database/requirements.txt
```
