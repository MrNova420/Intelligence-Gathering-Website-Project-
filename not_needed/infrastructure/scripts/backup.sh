#!/bin/bash

# Backup script for Intelligence Gathering Platform
# Creates backups of database and important files

set -e

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="intelligence_platform_${DATE}"

echo "🗄️  Starting backup process..."

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup database
echo "📊 Backing up PostgreSQL database..."
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U postgres intelligence_db > "$BACKUP_DIR/${BACKUP_NAME}_database.sql"

# Backup Redis data
echo "🔄 Backing up Redis data..."
docker-compose -f docker-compose.prod.yml exec -T redis redis-cli --rdb /data/dump.rdb
docker cp intelligence_redis_prod:/data/dump.rdb "$BACKUP_DIR/${BACKUP_NAME}_redis.rdb"

# Backup configuration files
echo "⚙️  Backing up configuration files..."
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" \
    .env \
    docker-compose.prod.yml \
    infrastructure/ \
    --exclude=infrastructure/nginx/ssl/

# Backup uploaded files (if any)
if [ -d "uploads" ]; then
    echo "📁 Backing up uploaded files..."
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" uploads/
fi

# Create backup info file
cat > "$BACKUP_DIR/${BACKUP_NAME}_info.txt" << EOF
Backup Information
==================
Date: $(date)
Backup Name: $BACKUP_NAME
Database: intelligence_db
Redis: included
Config: included
Uploads: $([ -d "uploads" ] && echo "included" || echo "none")

Files:
- ${BACKUP_NAME}_database.sql
- ${BACKUP_NAME}_redis.rdb  
- ${BACKUP_NAME}_config.tar.gz
$([ -d "uploads" ] && echo "- ${BACKUP_NAME}_uploads.tar.gz")
EOF

# Compress all backup files
echo "📦 Compressing backup..."
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_complete.tar.gz" \
    -C "$BACKUP_DIR" \
    "${BACKUP_NAME}_database.sql" \
    "${BACKUP_NAME}_redis.rdb" \
    "${BACKUP_NAME}_config.tar.gz" \
    "${BACKUP_NAME}_info.txt" \
    $([ -f "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" ] && echo "${BACKUP_NAME}_uploads.tar.gz")

# Clean up individual files
rm -f "$BACKUP_DIR/${BACKUP_NAME}_database.sql" \
      "$BACKUP_DIR/${BACKUP_NAME}_redis.rdb" \
      "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" \
      "$BACKUP_DIR/${BACKUP_NAME}_info.txt"
[ -f "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" ] && rm -f "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz"

# Clean old backups (keep last 7 days)
echo "🧹 Cleaning old backups..."
find $BACKUP_DIR -name "intelligence_platform_*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed successfully!"
echo "📁 Backup saved as: $BACKUP_DIR/${BACKUP_NAME}_complete.tar.gz"
echo "💾 Backup size: $(du -h "$BACKUP_DIR/${BACKUP_NAME}_complete.tar.gz" | cut -f1)"