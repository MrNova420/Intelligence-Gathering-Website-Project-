# Scripts - Intelligence Gathering Platform

This directory contains deployment, setup, and utility scripts for the Intelligence Gathering Platform.

## 📁 Scripts Overview

### 🚀 Startup Scripts
- **`start_platform.sh`** - Complete platform startup (recommended)
- **`start_backend.sh`** - Backend-only startup
- **`start_frontend.sh`** - Frontend-only startup
- **`easy_start.sh`** - Simplified startup with automatic setup
- **`start_termux.sh`** - Termux/Android optimized startup
- **`start_with_docker.sh`** - Docker-based startup

### ⚙️ Setup & Configuration
- **`setup.py`** - Automated platform setup and configuration
- **`start.sh`** - Simple startup wrapper

### 🚢 Deployment
- **`deploy_to_production.sh`** - Production deployment automation

## 🚀 Quick Start Options

### Simple Start (Recommended)
```bash
# From project root
./scripts/easy_start.sh
```

### Platform Components
```bash
# Complete platform
./scripts/start_platform.sh

# Backend only
./scripts/start_backend.sh

# Frontend only  
./scripts/start_frontend.sh
```

### Environment-Specific
```bash
# Termux/Android
./scripts/start_termux.sh

# Docker deployment
./scripts/start_with_docker.sh
```

## 🛠️ Setup

### First-Time Setup
```bash
# Automated setup
python scripts/setup.py

# Then start the platform
./scripts/easy_start.sh
```

## 🚢 Production Deployment

```bash
# Deploy to production
./scripts/deploy_to_production.sh
```

## 📋 Requirements

### System Requirements
- Python 3.8+
- Node.js 16+ (for frontend)
- Git
- Optional: Docker (for containerized deployment)

### Platform-Specific
- **Linux/macOS**: All scripts supported
- **Termux/Android**: Use `start_termux.sh`
- **Windows**: Use equivalent Python commands

## 🔧 Configuration

Scripts automatically handle:
- Dependency installation
- Environment configuration
- Database setup
- Service startup
- Health checks

## 🆘 Troubleshooting

If startup fails:
1. Check system requirements
2. Run setup script: `python scripts/setup.py`
3. Check logs for specific error messages
4. Use platform-specific scripts (e.g., `start_termux.sh`)

## 📝 Notes

- Scripts are designed to be idempotent (safe to run multiple times)
- Automatic dependency checking and installation
- Graceful error handling with helpful messages
- Support for multiple deployment environments