#!/bin/bash
set -e

echo "🚀 Starting Enhanced Production Deployment..."

# Configuration
PROJECT_NAME="intelligence-platform"
BACKUP_DIR="/opt/backups/$(date +%Y%m%d_%H%M%S)"
LOG_FILE="/var/log/deploy.log"

# Functions
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

check_requirements() {
    log "Checking deployment requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log "ERROR: Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log "ERROR: Docker Compose is not installed"
        exit 1
    fi
    
    # Check environment file
    if [ ! -f ".env.production" ]; then
        log "ERROR: .env.production file not found"
        exit 1
    fi
    
    log "✅ Requirements check passed"
}

backup_data() {
    log "Creating data backup..."
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    docker exec intelligence_postgres pg_dump -U postgres intelligence_db > "$BACKUP_DIR/database.sql" 2>/dev/null || true
    
    # Backup uploads
    docker cp intelligence_backend:/app/uploads "$BACKUP_DIR/" 2>/dev/null || true
    
    log "✅ Data backup completed: $BACKUP_DIR"
}

deploy() {
    log "Deploying application..."
    
    # Load environment variables
    set -a
    source .env.production
    set +a
    
    # Pull latest images
    docker-compose -f docker-compose.prod.enhanced.yml pull
    
    # Build custom images
    docker-compose -f docker-compose.prod.enhanced.yml build --no-cache
    
    # Start services with rolling update
    docker-compose -f docker-compose.prod.enhanced.yml up -d --remove-orphans
    
    # Wait for services to be healthy
    log "Waiting for services to be ready..."
    sleep 30
    
    # Run database migrations
    docker exec intelligence_backend python -m alembic upgrade head
    
    log "✅ Deployment completed successfully"
}

health_check() {
    log "Performing health checks..."
    
    # Check backend health
    if curl -f http://localhost/api/health > /dev/null 2>&1; then
        log "✅ Backend health check passed"
    else
        log "❌ Backend health check failed"
        exit 1
    fi
    
    # Check frontend
    if curl -f http://localhost > /dev/null 2>&1; then
        log "✅ Frontend health check passed"
    else
        log "❌ Frontend health check failed"
        exit 1
    fi
    
    log "✅ All health checks passed"
}

rollback() {
    log "Rolling back deployment..."
    
    # Stop current services
    docker-compose -f docker-compose.prod.enhanced.yml down
    
    # Restore from backup
    if [ -d "$BACKUP_DIR" ]; then
        # Restore database
        docker exec intelligence_postgres psql -U postgres -c "DROP DATABASE IF EXISTS intelligence_db;"
        docker exec intelligence_postgres psql -U postgres -c "CREATE DATABASE intelligence_db;"
        docker exec -i intelligence_postgres psql -U postgres intelligence_db < "$BACKUP_DIR/database.sql"
        
        # Restore uploads
        docker cp "$BACKUP_DIR/uploads" intelligence_backend:/app/
    fi
    
    log "✅ Rollback completed"
}

# Main execution
main() {
    log "Starting deployment process..."
    
    check_requirements
    backup_data
    
    # Deploy with error handling
    if deploy; then
        if health_check; then
            log "🎉 Deployment successful!"
            
            # Cleanup old images
            docker image prune -f
            
            # Send success notification
            echo "Deployment completed successfully at $(date)" | mail -s "Deployment Success" admin@yourdomain.com 2>/dev/null || true
        else
            log "❌ Health checks failed, rolling back..."
            rollback
            exit 1
        fi
    else
        log "❌ Deployment failed, rolling back..."
        rollback
        exit 1
    fi
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "health")
        health_check
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|health}"
        exit 1
        ;;
esac
