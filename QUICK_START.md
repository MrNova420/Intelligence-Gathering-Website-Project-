# 🚀 Intelligence Gathering Platform - Quick Start Guide

This guide will get you up and running with the Intelligence Gathering Platform in minutes!

## 🎯 Two Setup Options

### Option 1: Automated Local Setup (Recommended)
Run the automated setup script that handles everything for you:

```bash
python3 local_setup.py
```

Then start the platform:
```bash
./start_platform.sh
```

### Option 2: Manual Setup
Follow the manual steps below if you prefer to set up each component individually.

---

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.9+** - [Download here](https://python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)
- **Docker** (optional) - [Download here](https://docker.com/)

---

## 🏠 Local Development Setup (Manual)

### 1. Clone Repository
```bash
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
DATABASE_URL=sqlite:///./intelligence_platform.db
REDIS_URL=redis://localhost:6379/0
USE_REDIS_FALLBACK=true
SECRET_KEY=local-development-key-change-in-production
DEBUG=true
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000"]
EOF

cd ..
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
EOF

cd ..
```

### 4. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the Platform
- **Frontend (Main Website)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🐳 Docker Setup (Alternative)

For a containerized setup:

```bash
# Start everything with Docker
docker-compose -f docker-compose.dev.yml up --build

# Or use the provided script
./start_with_docker.sh
```

---

## 🌐 Production Deployment Guide

### Cloud Platforms

#### 🔵 Digital Ocean / Linode / VPS
```bash
# 1. Set up server (Ubuntu 20.04+)
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose nginx certbot python3-certbot-nginx

# 2. Clone repository
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# 3. Configure production environment
cp .env.example .env
# Edit .env with your production settings

# 4. Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d

# 5. Set up SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

#### ☁️ AWS / Google Cloud / Azure
```bash
# 1. Launch VM instance (t3.medium or larger)
# 2. Configure security groups (ports 80, 443, 22)
# 3. Follow VPS setup above
# 4. Configure load balancer if needed
```

#### 🟣 Heroku
```bash
# 1. Install Heroku CLI
# 2. Create apps
heroku create your-app-backend
heroku create your-app-frontend

# 3. Deploy backend
cd backend
git subtree push --prefix=backend heroku main

# 4. Deploy frontend
cd frontend
git subtree push --prefix=frontend heroku main

# 5. Configure environment variables in Heroku dashboard
```

#### ▲ Vercel (Frontend) + Railway (Backend)
```bash
# Frontend on Vercel:
# 1. Connect GitHub repo to Vercel
# 2. Set build command: cd frontend && npm run build
# 3. Set environment variables

# Backend on Railway:
# 1. Connect GitHub repo to Railway
# 2. Set start command: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
# 3. Set environment variables
```

---

## 🔒 Production Security Checklist

Before going live, ensure you:

- [ ] Change all default passwords
- [ ] Set strong `SECRET_KEY` in environment
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper database (PostgreSQL)
- [ ] Configure Redis for caching
- [ ] Set up backup system
- [ ] Configure monitoring and logging
- [ ] Review CORS settings
- [ ] Set up rate limiting
- [ ] Configure firewall rules

---

## 📊 Performance Optimization

For production deployments:

1. **Database**: Use PostgreSQL instead of SQLite
2. **Caching**: Set up Redis
3. **CDN**: Use CloudFlare or similar
4. **Monitoring**: Set up Grafana/Prometheus
5. **Backups**: Automated daily backups
6. **Scaling**: Use load balancers for high traffic

---

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :3000  # or :8000
# Kill process
kill -9 <PID>
```

**Dependencies not installing:**
```bash
# Clear npm cache
npm cache clean --force

# Clear pip cache
pip cache purge
```

**Database connection issues:**
```bash
# Check if database service is running
sudo systemctl status postgresql
sudo systemctl status redis
```

**Permission denied on scripts:**
```bash
chmod +x start_platform.sh
chmod +x start_backend.sh
chmod +x start_frontend.sh
```

---

## 📞 Support

- **Documentation**: Check the `/docs` folder
- **Issues**: Open a GitHub issue
- **API Reference**: http://localhost:8000/docs (when running)

---

## 🎉 You're Ready!

Your Intelligence Gathering Platform is now ready for use! The platform includes:

- 🔍 **100+ Scanner Tools** for intelligence gathering
- 🧠 **AI-Powered Analysis** with threat detection
- 📊 **Real-time Dashboard** with live metrics
- 🔒 **Enterprise Security** with encrypted data
- 📱 **Responsive Design** for all devices
- 🚀 **High Performance** with optimized backend

**Happy Intelligence Gathering! 🕵️‍♂️**