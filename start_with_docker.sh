#!/bin/bash
# Quick Docker setup for Intelligence Gathering Platform
echo "🐳 Starting Intelligence Gathering Platform with Docker..."

# Build and start services
docker-compose -f docker-compose.dev.yml up --build

echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
