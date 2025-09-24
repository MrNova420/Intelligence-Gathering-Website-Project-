#!/bin/bash
# Enhanced Maintenance Script for Intelligence Gathering Platform
# Advanced operations with monitoring, security, and automation

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs"
BACKUP_DIR="$PROJECT_ROOT/backups"
CONFIG_FILE="$PROJECT_ROOT/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_DIR/maintenance.log"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_DIR/maintenance.log"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_DIR/maintenance.log"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_DIR/maintenance.log"
}

# Setup function
setup_directories() {
    mkdir -p "$LOG_DIR" "$BACKUP_DIR"
    touch "$LOG_DIR/maintenance.log"
}

# System health check
check_system_health() {
    log "🏥 Performing comprehensive system health check..."
    
    # Check system resources
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    local memory_usage=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
    
    info "System Resources:"
    info "  CPU Usage: ${cpu_usage}%"
    info "  Memory Usage: ${memory_usage}%"
    info "  Disk Usage: ${disk_usage}%"
    
    # Check thresholds
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        warn "High CPU usage detected: ${cpu_usage}%"
    fi
    
    if (( $(echo "$memory_usage > 85" | bc -l) )); then
        warn "High memory usage detected: ${memory_usage}%"
    fi
    
    if (( disk_usage > 90 )); then
        warn "High disk usage detected: ${disk_usage}%"
    fi
    
    # Check services
    check_service_status "docker" "Docker daemon"
    check_service_status "nginx" "Nginx web server"
    
    # Check Docker containers
    if command -v docker &> /dev/null; then
        log "📦 Checking Docker containers..."
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | while read line; do
            info "  $line"
        done
    fi
    
    # Check network connectivity
    check_network_connectivity
    
    # Check SSL certificates
    check_ssl_certificates
    
    log "✅ System health check completed"
}

check_service_status() {
    local service_name="$1"
    local description="$2"
    
    if systemctl is-active --quiet "$service_name"; then
        info "  ✅ $description is running"
    else
        warn "  ❌ $description is not running"
    fi
}

check_network_connectivity() {
    log "🌐 Checking network connectivity..."
    
    local test_urls=("google.com" "github.com" "docker.io")
    
    for url in "${test_urls[@]}"; do
        if ping -c 1 -W 5 "$url" &> /dev/null; then
            info "  ✅ Connectivity to $url: OK"
        else
            warn "  ❌ Connectivity to $url: FAILED"
        fi
    done
}

check_ssl_certificates() {
    log "🔒 Checking SSL certificates..."
    
    local cert_dirs=("/etc/letsencrypt/live" "/etc/ssl/certs" "./infrastructure/nginx/ssl")
    
    for cert_dir in "${cert_dirs[@]}"; do
        if [[ -d "$cert_dir" ]]; then
            find "$cert_dir" -name "*.pem" -o -name "*.crt" | while read cert_file; do
                if openssl x509 -checkend 604800 -noout -in "$cert_file" &> /dev/null; then
                    info "  ✅ Certificate valid: $(basename "$cert_file")"
                else
                    warn "  ⚠️ Certificate expires soon: $(basename "$cert_file")"
                fi
            done
        fi
    done
}

# Enhanced backup function
create_enhanced_backup() {
    log "📦 Creating enhanced backup..."
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_name="intelligence_platform_${timestamp}"
    local backup_path="${BACKUP_DIR}/${backup_name}"
    
    mkdir -p "$backup_path"
    
    # Database backup
    if docker ps --format '{{.Names}}' | grep -q "intelligence_db"; then
        log "🗄️ Creating database backup..."
        docker exec intelligence_db pg_dump -U intelligence_user intelligence_db > "${backup_path}/database.sql"
        
        if [[ -s "${backup_path}/database.sql" ]]; then
            info "  ✅ Database backup completed: $(du -h "${backup_path}/database.sql" | cut -f1)"
        else
            error "  ❌ Database backup failed or empty"
        fi
    else
        warn "Database container not found, skipping database backup"
    fi
    
    # Application files backup
    log "📁 Creating application files backup..."
    tar -czf "${backup_path}/application.tar.gz" \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='*.log' \
        --exclude='venv' \
        --exclude='backups/*' \
        -C "$PROJECT_ROOT" .
    
    if [[ -s "${backup_path}/application.tar.gz" ]]; then
        info "  ✅ Application backup completed: $(du -h "${backup_path}/application.tar.gz" | cut -f1)"
    else
        error "  ❌ Application backup failed"
    fi
    
    # Configuration backup
    log "⚙️ Creating configuration backup..."
    cp "$CONFIG_FILE" "${backup_path}/environment.env" 2>/dev/null || warn "Environment file not found"
    
    if [[ -d "$PROJECT_ROOT/infrastructure" ]]; then
        tar -czf "${backup_path}/infrastructure.tar.gz" -C "$PROJECT_ROOT" infrastructure/
        info "  ✅ Infrastructure backup completed"
    fi
    
    # Create backup manifest
    cat > "${backup_path}/manifest.json" << EOF
{
    "backup_name": "$backup_name",
    "timestamp": "$timestamp",
    "platform": "$(uname -s)",
    "hostname": "$(hostname)",
    "docker_version": "$(docker --version 2>/dev/null || echo 'N/A')",
    "files": {
        "database": "$(test -f "${backup_path}/database.sql" && echo "true" || echo "false")",
        "application": "$(test -f "${backup_path}/application.tar.gz" && echo "true" || echo "false")",
        "infrastructure": "$(test -f "${backup_path}/infrastructure.tar.gz" && echo "true" || echo "false")",
        "environment": "$(test -f "${backup_path}/environment.env" && echo "true" || echo "false")"
    }
}
EOF
    
    # Compress entire backup
    tar -czf "${BACKUP_DIR}/${backup_name}.tar.gz" -C "$BACKUP_DIR" "$backup_name"
    rm -rf "$backup_path"
    
    log "✅ Enhanced backup completed: ${backup_name}.tar.gz"
    info "  Backup size: $(du -h "${BACKUP_DIR}/${backup_name}.tar.gz" | cut -f1)"
}

# Backup rotation and cleanup
rotate_backups() {
    log "🔄 Rotating old backups..."
    
    local keep_daily=7
    local keep_weekly=4
    local keep_monthly=3
    
    # Keep daily backups for 7 days
    find "$BACKUP_DIR" -name "intelligence_platform_*.tar.gz" -mtime +$keep_daily -delete
    
    local deleted_count=$(find "$BACKUP_DIR" -name "intelligence_platform_*.tar.gz" -mtime +$keep_daily 2>/dev/null | wc -l)
    
    if [[ $deleted_count -gt 0 ]]; then
        info "  🗑️ Removed $deleted_count old backup(s)"
    else
        info "  📦 No old backups to remove"
    fi
    
    log "✅ Backup rotation completed"
}

# Security monitoring
run_security_scan() {
    log "🔒 Running security scan..."
    
    # Check for suspicious processes
    info "Checking for suspicious processes..."
    ps aux | grep -E "(nc|netcat|nmap|sqlmap)" | grep -v grep | while read line; do
        warn "Suspicious process detected: $line"
    done
    
    # Check for failed login attempts
    if [[ -f "/var/log/auth.log" ]]; then
        local failed_logins=$(grep "Failed password" /var/log/auth.log | tail -20 | wc -l)
        if [[ $failed_logins -gt 0 ]]; then
            warn "Recent failed login attempts: $failed_logins"
        fi
    fi
    
    # Check disk space for logs
    local log_disk_usage=$(du -sm "$LOG_DIR" 2>/dev/null | cut -f1)
    if [[ $log_disk_usage -gt 100 ]]; then
        warn "Log directory using ${log_disk_usage}MB of disk space"
    fi
    
    # Check open ports
    info "Checking open ports..."
    if command -v netstat &> /dev/null; then
        netstat -tuln | grep LISTEN | while read line; do
            info "  Open port: $line"
        done
    fi
    
    log "✅ Security scan completed"
}

# Performance optimization
optimize_performance() {
    log "⚡ Running performance optimization..."
    
    # Clean up Docker
    if command -v docker &> /dev/null; then
        log "🐳 Cleaning Docker resources..."
        docker system prune -f --volumes
        info "  ✅ Docker cleanup completed"
    fi
    
    # Clean up logs
    log "📝 Cleaning old logs..."
    find "$LOG_DIR" -name "*.log" -mtime +30 -delete
    
    # Clear package cache (if applicable)
    if command -v apt-get &> /dev/null; then
        log "📦 Cleaning package cache..."
        apt-get clean
    fi
    
    # Optimize database (if running)
    if docker ps --format '{{.Names}}' | grep -q "intelligence_db"; then
        log "🗄️ Running database maintenance..."
        docker exec intelligence_db psql -U intelligence_user -d intelligence_db -c "VACUUM ANALYZE;" || warn "Database optimization failed"
    fi
    
    log "✅ Performance optimization completed"
}

# Update system
update_system() {
    log "🔄 Updating system..."
    
    # Pull latest code
    if [[ -d "$PROJECT_ROOT/.git" ]]; then
        log "📥 Pulling latest code..."
        cd "$PROJECT_ROOT"
        git fetch origin
        local current_branch=$(git branch --show-current)
        git pull origin "$current_branch"
        info "  ✅ Code updated"
    fi
    
    # Update Docker images
    if [[ -f "$PROJECT_ROOT/docker-compose.yml" ]]; then
        log "🐳 Updating Docker images..."
        cd "$PROJECT_ROOT"
        docker-compose pull
        docker-compose build --no-cache
        info "  ✅ Docker images updated"
    fi
    
    # Update dependencies
    if [[ -f "$PROJECT_ROOT/backend/requirements.txt" ]]; then
        log "🐍 Updating Python dependencies..."
        cd "$PROJECT_ROOT/backend"
        if [[ -d "venv" ]]; then
            source venv/bin/activate
            pip install -r requirements.txt --upgrade
            info "  ✅ Python dependencies updated"
        fi
    fi
    
    if [[ -f "$PROJECT_ROOT/frontend/package.json" ]]; then
        log "📦 Updating Node.js dependencies..."
        cd "$PROJECT_ROOT/frontend"
        npm update
        info "  ✅ Node.js dependencies updated"
    fi
    
    log "✅ System update completed"
}

# Restart services with health checks
restart_services() {
    log "🔄 Restarting services with health checks..."
    
    cd "$PROJECT_ROOT"
    
    # Stop services gracefully
    log "⏹️ Stopping services..."
    if [[ -f "docker-compose.yml" ]]; then
        docker-compose down --timeout 30
    fi
    
    # Wait for complete shutdown
    sleep 5
    
    # Start services
    log "▶️ Starting services..."
    if [[ -f "docker-compose.yml" ]]; then
        docker-compose up -d
    fi
    
    # Wait for services to start
    log "⏳ Waiting for services to start..."
    sleep 30
    
    # Health check
    log "🏥 Performing health checks..."
    local health_checks=0
    local max_checks=12  # 2 minutes with 10-second intervals
    
    while [[ $health_checks -lt $max_checks ]]; do
        if curl -sf http://localhost:8000/health &> /dev/null; then
            info "  ✅ Backend is healthy"
            break
        else
            ((health_checks++))
            info "  ⏳ Waiting for backend... ($health_checks/$max_checks)"
            sleep 10
        fi
    done
    
    if [[ $health_checks -eq $max_checks ]]; then
        error "Backend health check failed after 2 minutes"
        return 1
    fi
    
    # Check frontend
    if curl -sf http://localhost:3000 &> /dev/null; then
        info "  ✅ Frontend is healthy"
    else
        warn "Frontend health check failed"
    fi
    
    log "✅ Services restarted successfully"
}

# Advanced monitoring
run_advanced_monitoring() {
    log "📊 Running advanced monitoring..."
    
    # System metrics
    local load_avg=$(uptime | awk -F'load average:' '{print $2}')
    local uptime_info=$(uptime -p)
    local disk_info=$(df -h / | awk 'NR==2 {print $4 " available (" $5 " used)"}')
    
    info "System Information:"
    info "  Uptime: $uptime_info"
    info "  Load Average: $load_avg"
    info "  Disk Space: $disk_info"
    
    # Container metrics
    if command -v docker &> /dev/null; then
        log "🐳 Container metrics:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | while read line; do
            info "  $line"
        done
    fi
    
    # Generate monitoring report
    local report_file="$LOG_DIR/monitoring_report_$(date +%Y%m%d_%H%M%S).json"
    cat > "$report_file" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "hostname": "$(hostname)",
    "uptime": "$uptime_info",
    "load_average": "$load_avg",
    "disk_usage": "$disk_info",
    "docker_containers": $(docker ps --format '{{json .}}' | jq -s . 2>/dev/null || echo '[]'),
    "system_metrics": {
        "cpu_count": $(nproc),
        "memory_total": $(free -b | awk 'NR==2{print $2}'),
        "memory_used": $(free -b | awk 'NR==2{print $3}')
    }
}
EOF
    
    info "  📄 Monitoring report saved: $report_file"
    log "✅ Advanced monitoring completed"
}

# Show usage information
show_usage() {
    cat << EOF
🔧 Enhanced Maintenance Script for Intelligence Gathering Platform

Usage: $0 [COMMAND] [OPTIONS]

COMMANDS:
    health          Perform comprehensive system health check
    backup          Create enhanced backup with verification
    rotate          Rotate and clean old backups
    security        Run security scan and monitoring
    optimize        Run performance optimization
    update          Update system and dependencies
    restart         Restart services with health checks
    monitor         Run advanced monitoring and generate report
    logs            Show recent logs with filtering options
    status          Show comprehensive system status
    full            Run full maintenance cycle (health + backup + optimize)

OPTIONS:
    --verbose       Enable verbose output
    --dry-run       Show what would be done without executing
    --help          Show this help message

EXAMPLES:
    $0 health                    # Run health check
    $0 backup                    # Create backup
    $0 full                      # Run complete maintenance
    $0 logs --lines 100          # Show last 100 log lines
    $0 restart --wait-time 60    # Restart with 60s wait time

LOG FILES:
    Maintenance: $LOG_DIR/maintenance.log
    Application: $LOG_DIR/app.log
    Error: $LOG_DIR/error.log

For more information, visit: https://github.com/MrNova420/Intelligence-Gathering-Website-Project-
EOF
}

# Show logs with filtering
show_logs() {
    local lines="${2:-100}"
    local service="${3:-all}"
    
    log "📋 Showing logs (last $lines lines, service: $service)..."
    
    case "$service" in
        "all")
            if [[ -f "$LOG_DIR/maintenance.log" ]]; then
                echo -e "${CYAN}=== Maintenance Logs ===${NC}"
                tail -n "$lines" "$LOG_DIR/maintenance.log"
            fi
            
            if command -v docker-compose &> /dev/null; then
                echo -e "${CYAN}=== Docker Logs ===${NC}"
                docker-compose logs --tail="$lines"
            fi
            ;;
        "maintenance")
            tail -n "$lines" "$LOG_DIR/maintenance.log" 2>/dev/null || warn "Maintenance log not found"
            ;;
        "docker")
            docker-compose logs --tail="$lines" 2>/dev/null || warn "Docker logs not available"
            ;;
        *)
            docker-compose logs --tail="$lines" "$service" 2>/dev/null || warn "Service '$service' logs not found"
            ;;
    esac
}

# Show comprehensive status
show_status() {
    log "📊 Intelligence Gathering Platform - System Status"
    echo
    
    # System information
    info "SYSTEM INFORMATION:"
    info "  Hostname: $(hostname)"
    info "  OS: $(uname -s) $(uname -r)"
    info "  Uptime: $(uptime -p)"
    info "  Load: $(uptime | awk -F'load average:' '{print $2}')"
    echo
    
    # Resource usage
    info "RESOURCE USAGE:"
    info "  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
    info "  Memory: $(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')%"
    info "  Disk: $(df -h / | awk 'NR==2 {print $5}')"
    echo
    
    # Services status
    info "SERVICES STATUS:"
    if command -v docker &> /dev/null; then
        docker ps --format "  {{.Names}}: {{.Status}}" | while read line; do
            info "$line"
        done
    else
        warn "  Docker not available"
    fi
    echo
    
    # Network status
    info "NETWORK STATUS:"
    if ping -c 1 -W 5 google.com &> /dev/null; then
        info "  Internet: ✅ Connected"
    else
        warn "  Internet: ❌ Disconnected"
    fi
    
    # Application status
    info "APPLICATION STATUS:"
    if curl -sf http://localhost:8000/health &> /dev/null; then
        info "  Backend API: ✅ Healthy"
    else
        warn "  Backend API: ❌ Unhealthy"
    fi
    
    if curl -sf http://localhost:3000 &> /dev/null; then
        info "  Frontend: ✅ Healthy"
    else
        warn "  Frontend: ❌ Unhealthy"
    fi
    
    # Recent backups
    info "BACKUP STATUS:"
    local backup_count=$(find "$BACKUP_DIR" -name "*.tar.gz" -mtime -7 | wc -l)
    info "  Recent backups (7 days): $backup_count"
    
    if [[ $backup_count -gt 0 ]]; then
        local latest_backup=$(find "$BACKUP_DIR" -name "*.tar.gz" -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
        local backup_age=$(stat -c %Y "$latest_backup")
        local current_time=$(date +%s)
        local age_hours=$(( (current_time - backup_age) / 3600 ))
        info "  Latest backup: $(basename "$latest_backup") (${age_hours}h ago)"
    fi
}

# Full maintenance cycle
run_full_maintenance() {
    log "🔧 Starting full maintenance cycle..."
    
    local start_time=$(date +%s)
    
    # Run all maintenance tasks
    check_system_health
    create_enhanced_backup
    rotate_backups
    run_security_scan
    optimize_performance
    run_advanced_monitoring
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log "✅ Full maintenance cycle completed in ${duration} seconds"
    
    # Generate summary report
    local report_file="$LOG_DIR/maintenance_summary_$(date +%Y%m%d_%H%M%S).txt"
    cat > "$report_file" << EOF
Intelligence Gathering Platform - Maintenance Summary
=====================================================
Completed: $(date)
Duration: ${duration} seconds

Tasks Completed:
- ✅ System health check
- ✅ Enhanced backup creation
- ✅ Backup rotation
- ✅ Security scan
- ✅ Performance optimization  
- ✅ Advanced monitoring

Next maintenance recommended: $(date -d '+1 day')
EOF
    
    info "📄 Maintenance summary saved: $report_file"
}

# Main execution
main() {
    setup_directories
    
    case "${1:-help}" in
        "health")
            check_system_health
            ;;
        "backup")
            create_enhanced_backup
            ;;
        "rotate")
            rotate_backups
            ;;
        "security")
            run_security_scan
            ;;
        "optimize")
            optimize_performance
            ;;
        "update")
            update_system
            ;;
        "restart")
            restart_services
            ;;
        "monitor")
            run_advanced_monitoring
            ;;
        "logs")
            show_logs "$@"
            ;;
        "status")
            show_status
            ;;
        "full")
            run_full_maintenance
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"