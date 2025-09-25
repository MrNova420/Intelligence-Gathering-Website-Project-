#!/bin/bash

# Production deployment script for Intelligence Gathering Platform
# This script sets up a secure production environment

set -e

echo "🚀 Starting Intelligence Gathering Platform Production Deployment"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root for security reasons"
   exit 1
fi

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup environment
echo "🔧 Setting up environment..."

# Copy environment template if .env doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file from template. Please edit it with your settings."
    echo "⚠️  IMPORTANT: Update all passwords and API keys in .env file before continuing!"
    read -p "Press Enter after updating .env file..."
fi

# Create necessary directories
mkdir -p infrastructure/nginx/ssl
mkdir -p logs
mkdir -p backups

# Generate SSL certificates if they don't exist
if [ ! -f infrastructure/nginx/ssl/cert.pem ]; then
    echo "🔐 Generating self-signed SSL certificates..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout infrastructure/nginx/ssl/key.pem \
        -out infrastructure/nginx/ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "✅ SSL certificates generated"
    echo "⚠️  For production, replace with proper SSL certificates from a CA"
fi

# Set proper permissions
chmod 600 infrastructure/nginx/ssl/key.pem
chmod 644 infrastructure/nginx/ssl/cert.pem

# Build and start services
echo "🏗️  Building and starting services..."

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Build custom images
docker-compose -f docker-compose.prod.yml build --no-cache

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check database
if docker-compose -f docker-compose.prod.yml exec -T postgres pg_isready -U postgres; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready"
    exit 1
fi

# Check Redis
if docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready"
    exit 1
fi

# Check backend API
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend API is ready"
else
    echo "❌ Backend API is not ready"
    exit 1
fi

# Check frontend
if curl -f http://localhost:3000 &> /dev/null; then
    echo "✅ Frontend is ready"
else
    echo "❌ Frontend is not ready"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "📊 Service Status:"
echo "Frontend: https://localhost:3000"
echo "Backend API: https://localhost:8000"
echo "API Documentation: https://localhost:8000/docs"
echo "Health Check: https://localhost:8000/health"
echo ""
echo "🔧 Management Commands:"
echo "View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "Stop services: docker-compose -f docker-compose.prod.yml down"
echo "Restart services: docker-compose -f docker-compose.prod.yml restart"
echo "Update services: ./scripts/update.sh"
echo ""
echo "🔐 Security Reminders:"
echo "1. Update all default passwords in .env file"
echo "2. Replace self-signed SSL certificates with proper CA certificates"
echo "3. Configure firewall to only allow necessary ports"
echo "4. Set up regular backups using ./scripts/backup.sh"
echo "5. Monitor logs regularly for security issues"
echo ""
echo "✅ Intelligence Gathering Platform is now running in production mode!"