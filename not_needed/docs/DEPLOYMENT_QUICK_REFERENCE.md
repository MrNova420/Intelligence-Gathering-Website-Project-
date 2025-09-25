# 🚀 Production Deployment - Quick Reference

## **⚡ One-Command Deploy Options**

```bash
# Interactive deployment script
./deploy_to_production.sh

# Quick options:
# 1 = Vercel + Railway (Free-$20/mo)
# 2 = DigitalOcean ($12-50/mo) 
# 3 = AWS ($50+/mo)
# 4 = Docker Production
# 5 = VPS Manual Setup
```

---

## **🏆 Recommended by Budget**

| Budget | Provider | Setup Time | Best For |
|--------|----------|------------|----------|
| **$0-20/mo** | Vercel + Railway | 30 min | MVP, Testing |
| **$12-50/mo** | DigitalOcean | 2-3 hrs | Small Business |
| **$50+/mo** | AWS/Azure/GCP | 4-6 hrs | Enterprise |

---

## **🚀 Quick Deploy (Vercel + Railway)**

```bash
# 1. Install CLIs
npm install -g @railway/cli vercel

# 2. Deploy backend (Railway)
railway login
railway init
railway up

# 3. Deploy frontend (Vercel)
vercel login
vercel

# 4. Set environment variables in dashboards
# Railway: DATABASE_URL, SECRET_KEY, ENVIRONMENT=production
# Vercel: REACT_APP_API_URL=https://your-app.railway.app
```

**Result**: Live website in 30 minutes, $0-20/month

---

## **🏗️ DigitalOcean Droplet**

```bash
# 1. Create droplet (Ubuntu 22.04, $12/mo minimum)
# 2. Upload deployment script
scp deploy_digitalocean.sh root@your-ip:~/

# 3. SSH and run setup
ssh root@your-ip
./deploy_digitalocean.sh

# 4. Configure domain and SSL
# Point domain to droplet IP
# certbot --nginx -d yourdomain.com
```

**Result**: Full control server, $12-50/month

---

## **☁️ AWS Complete Setup**

```bash
# 1. Install AWS CLI
pip install awscli
aws configure

# 2. Deploy infrastructure
aws cloudformation create-stack \
  --stack-name intelligence-platform \
  --template-body file://aws-infrastructure.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=your-key

# 3. Setup application on EC2
# (Detailed in PRODUCTION_DEPLOYMENT_GUIDE.md)
```

**Result**: Enterprise-scale deployment, $50+/month

---

## **🐳 Docker Production**

```bash
# 1. Setup production environment
cp .env.production.example .env.production
# Edit with your values

# 2. Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 3. Setup SSL certificates
# Add certificates to ssl/ directory
# Update nginx configuration
```

**Result**: Containerized deployment, works anywhere

---

## **🌐 Domain & SSL Setup**

```bash
# 1. Configure DNS (any domain provider)
A     @           your-server-ip
A     www         your-server-ip
CNAME api         your-backend-url

# 2. Get free SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 3. Verify HTTPS
curl https://yourdomain.com
```

---

## **⚙️ Essential Environment Variables**

```bash
# Production .env
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
ENVIRONMENT=production
FRONTEND_URL=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com

# Optional API keys
CLEARBIT_API_KEY=your-key
HUNTER_API_KEY=your-key
STRIPE_SECRET_KEY=your-key
```

---

## **🔒 Security Checklist**

```bash
# ✅ Must-have security
- [ ] HTTPS certificate installed
- [ ] Firewall configured (ufw/security groups)
- [ ] Strong passwords/keys (64+ characters)
- [ ] Database connections encrypted
- [ ] Environment variables secured
- [ ] Regular backups configured
- [ ] Monitoring/alerting setup
```

---

## **📊 Monitoring Commands**

```bash
# Check service status
systemctl status intelligence-backend
systemctl status nginx
systemctl status postgresql

# Monitor resources
htop                    # CPU, memory
df -h                   # Disk space
tail -f /var/log/nginx/error.log  # Nginx errors
journalctl -u intelligence-backend -f  # App logs

# Health check
curl https://yourdomain.com/api/health
```

---

## **🆘 Emergency Fixes**

```bash
# Service down
sudo systemctl restart intelligence-backend
sudo systemctl restart nginx

# High memory/CPU
sudo systemctl stop intelligence-backend
# Scale up server or optimize code
sudo systemctl start intelligence-backend

# Database issues
sudo systemctl restart postgresql
sudo -u postgres psql intelligence_platform

# SSL certificate expired
sudo certbot renew --nginx
```

---

## **💰 Cost Optimization**

| Optimization | Savings | Impact |
|--------------|---------|---------|
| **CDN (CloudFlare)** | 30-50% | Faster loading |
| **Database optimization** | 20-40% | Better performance |
| **Image compression** | 10-20% | Reduced bandwidth |
| **Caching (Redis)** | 40-60% | Much faster responses |

---

## **📈 Scaling Triggers**

**Scale up when:**
- Response time consistently > 2 seconds
- CPU usage > 80% for 5+ minutes  
- Memory usage > 90%
- Error rate > 1%

**Scaling options:**
```bash
# Vertical scaling (bigger server)
# Horizontal scaling (more servers + load balancer)
# Database scaling (read replicas)
# CDN for static content
```

---

## **🎯 Go-Live Checklist**

### **✅ Technical**
- [ ] Domain configured and pointing to server
- [ ] SSL certificate installed and auto-renewing
- [ ] Database backed up and optimized
- [ ] Monitoring and alerting configured
- [ ] Performance tested under load
- [ ] Security audit completed

### **✅ Content**
- [ ] Privacy Policy and Terms of Service
- [ ] Contact information and support
- [ ] Documentation complete and accessible
- [ ] User onboarding flow tested

### **✅ Business**
- [ ] Payment processing (if applicable)
- [ ] Analytics tracking (Google Analytics)
- [ ] Error tracking (Sentry)
- [ ] Customer support system ready

---

## **🎉 Launch Day**

```bash
# Final checks
./health_check.sh       # Should show 100%
curl https://yourdomain.com/api/health
curl https://yourdomain.com

# Monitor for 24 hours
# Check logs every few hours
# Respond to any user feedback

# Celebrate! 🎉 Your platform is live!
```

---

## **📞 Need Help?**

- **📖 Complete Guide**: [PRODUCTION_DEPLOYMENT_GUIDE.md](PRODUCTION_DEPLOYMENT_GUIDE.md)
- **🛠️ Setup Script**: `./deploy_to_production.sh`
- **📋 Platform Guide**: [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md)
- **🆘 Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)