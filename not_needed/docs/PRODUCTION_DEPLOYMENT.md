# 🌐 Production Deployment Guide

Complete guide for deploying the Intelligence Gathering Platform to production for public use.

## 🎯 Deployment Options

### 1. VPS/Cloud Server Deployment (Recommended)
### 2. Docker-based Deployment  
### 3. Platform-as-a-Service (PaaS)
### 4. Kubernetes Deployment

---

## 🚀 Option 1: VPS/Cloud Server (Digital Ocean, Linode, AWS EC2)

### Prerequisites
- Ubuntu 20.04+ server with at least 2GB RAM
- Domain name pointed to your server
- SSH access to the server

### Step 1: Server Setup
```bash
# Connect to your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx git

# Enable Docker
systemctl enable docker
systemctl start docker

# Add user to docker group (replace 'username' with your username)
usermod -aG docker $USER
```

### Step 2: Deploy Application
```bash
# Clone repository
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Copy and configure environment
cp .env.example .env

# Edit environment file with production settings
nano .env
```

**Important Environment Variables:**
```bash
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/intelligence_db
POSTGRES_USER=intelligence_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=intelligence_db

# Security
SECRET_KEY=your-super-secure-secret-key-here
ENVIRONMENT=production
DEBUG=false

# Domain
DOMAIN=yourdomain.com
CORS_ORIGINS=["https://yourdomain.com"]

# API Keys (optional)
CLEARBIT_API_KEY=your_key
HUNTER_API_KEY=your_key
STRIPE_SECRET_KEY=your_key
```

### Step 3: Start Services
```bash
# Start with production compose
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### Step 4: Configure Nginx
```bash
# Create Nginx configuration
cat > /etc/nginx/sites-available/intelligence-platform << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/intelligence-platform /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### Step 5: SSL Certificate
```bash
# Get SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
certbot renew --dry-run
```

### Step 6: Setup Monitoring & Backups
```bash
# Create backup script
cat > /root/backup.sh << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
mkdir -p \$BACKUP_DIR

# Backup database
docker exec intelligence_db pg_dump -U intelligence_user intelligence_db > \$BACKUP_DIR/db_\$DATE.sql

# Backup application data
tar -czf \$BACKUP_DIR/app_\$DATE.tar.gz /root/Intelligence-Gathering-Website-Project-

# Keep only last 7 days of backups
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /root/backup.sh

# Schedule daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /root/backup.sh") | crontab -
```

---

## 🐳 Option 2: Simple Docker Deployment

### Prerequisites
- Server with Docker and Docker Compose
- Domain name (optional)

### Quick Deploy
```bash
# Clone and configure
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## ☁️ Option 3: Platform-as-a-Service (PaaS)

### Heroku Deployment
```bash
# Install Heroku CLI
# Create apps
heroku create your-app-name-backend
heroku create your-app-name-frontend

# Configure environment variables
heroku config:set SECRET_KEY=your-secret -a your-app-name-backend
heroku config:set DATABASE_URL=postgres://... -a your-app-name-backend

# Deploy backend
git subtree push --prefix=backend heroku main

# Deploy frontend  
git subtree push --prefix=frontend heroku main
```

### Vercel + Railway/Render
```bash
# Frontend on Vercel:
# 1. Import GitHub repo to Vercel
# 2. Set framework preset to Next.js
# 3. Set root directory to 'frontend'
# 4. Configure environment variables

# Backend on Railway:
# 1. Connect GitHub repo to Railway
# 2. Set root directory to 'backend'
# 3. Configure environment variables
# 4. Deploy
```

---

## ☸️ Option 4: Kubernetes Deployment

### Prerequisites
- Kubernetes cluster
- kubectl configured
- Helm (optional)

### Deploy with Kubernetes
```bash
# Create namespace
kubectl create namespace intelligence-platform

# Apply configurations
kubectl apply -f infrastructure/k8s/

# Check deployment
kubectl get pods -n intelligence-platform
```

---

## 🔒 Security Hardening

### Essential Security Steps
1. **Change all default passwords**
2. **Configure firewall**:
   ```bash
   ufw allow ssh
   ufw allow http
   ufw allow https
   ufw enable
   ```
3. **Set up fail2ban**:
   ```bash
   apt install fail2ban
   systemctl enable fail2ban
   ```
4. **Regular updates**:
   ```bash
   # Add to crontab
   0 4 * * 1 apt update && apt upgrade -y
   ```
5. **Monitor logs**:
   ```bash
   # Check application logs
   docker-compose logs -f
   
   # Check system logs
   journalctl -fu nginx
   ```

---

## 📊 Performance Optimization

### Database Optimization
```bash
# PostgreSQL tuning
# Add to postgresql.conf:
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
```

### Caching
```bash
# Redis configuration
# Add to redis.conf:
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### CDN Setup
- Use CloudFlare for static assets
- Configure appropriate cache headers
- Enable compression

---

## 📈 Monitoring & Maintenance

### Health Checks
```bash
# API Health
curl https://yourdomain.com/api/health

# Frontend Health  
curl https://yourdomain.com/

# Database Health
docker exec intelligence_db pg_isready
```

### Log Management
```bash
# Application logs
docker-compose logs -f --tail=100

# System logs
journalctl -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Automated Monitoring
Set up monitoring with:
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: Sentry, LogRocket
- **Server monitoring**: New Relic, DataDog

---

## 🆘 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check memory
free -h
```

**Database connection issues:**
```bash
# Check database container
docker exec -it intelligence_db psql -U postgres

# Check connection from app
docker exec -it intelligence_api python -c "from app.db import engine; print(engine.execute('SELECT 1').scalar())"
```

**SSL certificate issues:**
```bash
# Renew certificate
certbot renew

# Check certificate status
certbot certificates
```

**High memory usage:**
```bash
# Check container resources
docker stats

# Restart services if needed
docker-compose restart
```

---

## 📞 Support & Maintenance

### Maintenance Schedule
- **Daily**: Monitor logs and performance
- **Weekly**: Check backups and updates
- **Monthly**: Security audit and dependency updates
- **Quarterly**: Performance optimization and scaling review

### Support Resources
- GitHub Issues for bug reports
- Documentation in `/docs` folder
- API documentation at `/api/docs`
- Server logs for troubleshooting

---

## 🎉 Deployment Complete!

Your Intelligence Gathering Platform is now live and ready for public use!

**Access URLs:**
- **Main Website**: https://yourdomain.com
- **API Documentation**: https://yourdomain.com/api/docs
- **Admin Interface**: https://yourdomain.com/admin

**Next Steps:**
1. Test all functionality
2. Set up monitoring
3. Configure backups
4. Review security settings
5. Plan for scaling

**Happy Intelligence Gathering! 🕵️‍♂️**