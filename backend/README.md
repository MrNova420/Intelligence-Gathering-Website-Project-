# Backend - Intelligence Gathering Platform

This directory contains the Python backend application for the Intelligence Gathering Platform.

## 📁 Structure

```
backend/
├── app/                    # FastAPI application code
│   ├── api/               # API routes and endpoints
│   ├── core/              # Core configuration and security
│   ├── db/                # Database models and migrations
│   ├── scanners/          # Intelligence gathering modules
│   └── services/          # Business logic services
├── tests/                  # Test suite
├── webapp.py              # Main unified web application
├── unified_app.py         # Primary entry point
├── run_standalone.py      # Standalone backend runner
├── config.py              # Configuration management
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### Main Application (Recommended)
```bash
# From project root
python start.py

# Or directly from backend
cd backend
python unified_app.py
```

### Standalone Backend Only
```bash
cd backend
python run_standalone.py
```

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Other dependencies in requirements.txt

## 🔧 Configuration

The application uses environment variables and configuration files:
- `.env` files for environment-specific settings
- `config.py` for centralized configuration management

## 🧪 Testing

```bash
cd backend
python -m pytest tests/
```

## 🌐 API Documentation

When running, API documentation is available at:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Features

- **Intelligence Gathering**: 100+ scanning modules
- **API-First Design**: Complete REST API
- **Security**: Enterprise-grade security features
- **Performance**: Multi-level caching and optimization
- **Compliance**: GDPR/CCPA compliance features
- **Monitoring**: Real-time performance monitoring