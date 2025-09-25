# 🚀 Intelligence Gathering Platform - Deployment Guide

## Overview
This guide covers the complete deployment of the Intelligence Gathering Platform from development to production. The platform is designed for enterprise-grade deployment with comprehensive security, performance optimization, and monitoring.

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Docker-compatible environment
- **CPU**: 4+ cores (8+ recommended for production)
- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 50GB+ SSD (100GB+ for production)
- **Network**: Stable internet connection for external API calls

### Software Dependencies
- **Python**: 3.9+
- **Node.js**: 16+
- **PostgreSQL**: 13+
- **Redis**: 6+
- **Docker & Docker Compose**: Latest stable versions

## 🔧 Development Setup

### 1. Repository Clone
```bash
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Database Setup
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb intelligence_platform
sudo -u postgres createuser --superuser intelligence_user
sudo -u postgres psql -c "ALTER USER intelligence_user PASSWORD 'your_secure_password';"
```

### 5. Redis Setup
```bash
# Install Redis
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 6. Environment Configuration
Create `.env` files:

**Backend `.env`:**
```env
DATABASE_URL=postgresql://intelligence_user:your_secure_password@localhost/intelligence_platform
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here
ENVIRONMENT=development
DEBUG=true
```

**Frontend `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python run_tests.py
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Integration Testing
```bash
# Start backend services
cd backend
python -m uvicorn app.main:app --reload

# Start frontend
cd frontend
npm run dev

# Test full workflow at http://localhost:3000
```

## 🐳 Docker Deployment

### 1. Docker Compose Setup
```bash
# Copy environment template
cp docker-compose.yml.example docker-compose.yml
cp .env.example .env

# Edit configuration
nano .env
```

### 2. Build and Deploy
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Docker Services
- **Backend API**: Port 8000
- **Frontend**: Port 3000
- **PostgreSQL**: Port 5432
- **Redis**: Port 6379

## 🌐 Production Deployment

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Security Hardening
```bash
# Create non-root user
sudo adduser intelligence
sudo usermod -aG docker intelligence

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. SSL/TLS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com
```

### 4. Production Environment Variables
```env
# Production .env
DATABASE_URL=postgresql://intelligence_user:production_password@postgres:5432/intelligence_platform
REDIS_URL=redis://redis:6379/0
SECRET_KEY=production_jwt_secret_256_bit_key
ENCRYPTION_KEY=production_aes_256_encryption_key
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 5. Database Migration
```bash
# Run database migrations
docker-compose exec backend python -m alembic upgrade head

# Create initial admin user
docker-compose exec backend python create_admin_user.py
```

## 📊 Monitoring & Maintenance

### 1. Health Checks
```bash
# API health check
curl http://localhost:8000/health

# Database connectivity
docker-compose exec backend python -c "from app.core.database import engine; print('DB OK' if engine else 'DB Error')"
```

### 2. Log Management
```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# System logs
sudo journalctl -u docker -f
```

### 3. Performance Monitoring
```bash
# Container resource usage
docker stats

# Database performance
docker-compose exec postgres pg_stat_activity

# Redis performance
docker-compose exec redis redis-cli info stats
```

### 4. Backup Strategy
```bash
# Database backup
docker-compose exec postgres pg_dump -U intelligence_user intelligence_platform > backup_$(date +%Y%m%d).sql

# Application data backup
docker-compose exec backend python backup_data.py

# Schedule automated backups
sudo crontab -e
# Add: 0 2 * * * /path/to/backup_script.sh
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database status
docker-compose exec postgres pg_isready

# Reset database
docker-compose down
docker volume rm intelligence-platform_postgres_data
docker-compose up -d postgres
```

#### 2. Redis Connection Issues
```bash
# Check Redis status
docker-compose exec redis redis-cli ping

# Clear Redis cache
docker-compose exec redis redis-cli flushall
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x backend/run_tests.py
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h
docker system df

# Clean up Docker
docker system prune -a
```

## 🛡️ Security Checklist

### Pre-Production Security
- [ ] Change all default passwords
- [ ] Generate secure JWT secret keys
- [ ] Configure SSL/TLS certificates
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Configure rate limiting
- [ ] Set up intrusion detection
- [ ] Review CORS settings
- [ ] Enable MFA for admin accounts
- [ ] Configure secure headers

### Ongoing Security
- [ ] Regular security updates
- [ ] Monitor failed login attempts
- [ ] Review audit logs weekly
- [ ] Rotate encryption keys quarterly
- [ ] Update SSL certificates
- [ ] Backup security configurations
- [ ] Test disaster recovery

## 🚀 Scaling & Performance

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  backend:
    deploy:
      replicas: 3
  frontend:
    deploy:
      replicas: 2
```

### Load Balancing
```bash
# Using nginx
sudo apt install nginx
# Configure upstream servers in nginx.conf
```

### Database Optimization
```sql
-- Recommended indexes
CREATE INDEX CONCURRENTLY idx_queries_user_created ON queries(user_id, created_at);
CREATE INDEX CONCURRENTLY idx_scan_results_query_scanner ON scan_results(query_id, scanner_type);
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### Cache Optimization
```python
# Redis optimization
REDIS_MAXMEMORY=4gb
REDIS_MAXMEMORY_POLICY=allkeys-lru
```

## 📈 Maintenance Schedule

### Daily
- Monitor system health
- Check application logs
- Verify backup completion
- Review security alerts

### Weekly  
- Update dependencies
- Review performance metrics
- Clean temporary files
- Test disaster recovery

### Monthly
- Security audit
- Performance optimization
- Capacity planning
- Documentation updates

### Quarterly
- Rotate encryption keys
- Security penetration testing
- Disaster recovery testing
- Architecture review

## 📞 Support & Resources

### Documentation
- [API Documentation](./API_DOCUMENTATION.md)
- [Security Guide](./SECURITY_GUIDE.md)
- [Performance Tuning](./PERFORMANCE_GUIDE.md)

### Monitoring Dashboards
- Application: http://localhost:3000/admin/dashboard
- System Health: http://localhost:8000/health
- Database: PostgreSQL logs
- Cache: Redis info

### Emergency Contacts
- **System Admin**: admin@yourdomain.com
- **Security Team**: security@yourdomain.com
- **On-call Support**: +1-xxx-xxx-xxxx

---

## 🎉 Deployment Complete!

Your Intelligence Gathering Platform is now ready for production use with:

✅ **Enterprise Security**: MFA, RBAC, encryption, audit logging
✅ **High Performance**: Redis caching, async processing, optimized queries
✅ **Monitoring**: Health checks, performance metrics, error tracking
✅ **Scalability**: Docker containers, horizontal scaling, load balancing
✅ **Compliance**: GDPR/CCPA ready, comprehensive audit trails

For additional support, refer to the documentation or contact the development team.