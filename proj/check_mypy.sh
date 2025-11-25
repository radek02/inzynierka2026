#!/bin/bash
# Run mypy checks for all modules

set -e

echo "Checking CommunicationService..."
mypy CommunicationService/

echo ""
echo "Checking RecommendationService..."
mypy RecommendationService/

echo ""
echo "Checking Cache..."
mypy Cache/cache_client.py

echo ""
echo "All mypy checks passed!"
