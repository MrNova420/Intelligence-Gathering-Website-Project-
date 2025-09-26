#!/bin/bash
# Maintenance Script for Intelligence Gathering Platform

echo "🔧 Intelligence Gathering Platform - Maintenance"

case "$1" in
    "backup")
        echo "📦 Creating backup..."
        docker exec intelligence_db pg_dump -U intelligence_user intelligence_db > "backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "✅ Backup completed"
        ;;
    "logs")
        echo "📋 Recent logs:"
        docker-compose logs --tail=100 -f
        ;;
    "restart")
        echo "🔄 Restarting services..."
        docker-compose restart
        echo "✅ Services restarted"
        ;;
    "update")
        echo "📦 Updating application..."
        git pull
        docker-compose build
        docker-compose up -d
        echo "✅ Update completed"
        ;;
    "status")
        echo "📊 Service status:"
        docker-compose ps
        ;;
    *)
        echo "Usage: $0 {backup|logs|restart|update|status}"
        exit 1
        ;;
esac
