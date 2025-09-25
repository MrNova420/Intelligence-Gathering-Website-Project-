# 🚀 Developer Setup Guide - Intelligence Gathering Platform

## Overview

This guide provides comprehensive instructions for setting up the Intelligence Gathering Platform development environment. The platform features a modern **Next.js 14 + React 18** frontend with **FastAPI + Python** backend, supporting **98+ scanner tools** and enterprise-grade security.

## Prerequisites

### Required Software

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Node.js** | 18.0+ | Frontend development | [Download](https://nodejs.org/) |
| **Python** | 3.9+ | Backend services | [Download](https://python.org/) |
| **Git** | Latest | Version control | [Download](https://git-scm.com/) |
| **Docker** | Latest | Containerization (optional) | [Download](https://docker.com/) |

### System Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Network**: Internet connection for API services

## Quick Start (5 Minutes)

### 1. Clone Repository

```bash
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
```

### 2. Automated Setup

Run the automated setup script:

```bash
# For Unix/Linux/macOS
./easy_start.sh

# For Windows
.\run.bat

# Or using Python
python setup.py
```

### 3. Manual Setup (If Automated Fails)

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -m alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Modern UI**: http://localhost:3000/modern

## Development Environment Setup

### Environment Variables

Create these files from the examples:

#### Backend (.env)

```bash
# Copy and configure
cp backend/.env.example backend/.env
```

Key variables to configure:

```env
# Database
DATABASE_URL=sqlite:///./intelligence_platform.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (Optional - for enhanced functionality)
CLEARBIT_API_KEY=your-clearbit-key
HUNTER_IO_API_KEY=your-hunter-key
GOOGLE_API_KEY=your-google-key

# Features
ENABLE_MONITORING=true
ENABLE_ERROR_TRACKING=true
ENABLE_AUTO_BACKUP=true
```

#### Frontend (.env.local)

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENV=development
```

### IDE Configuration

#### VS Code (Recommended)

Install these extensions:

```json
{
  "recommendations": [
    "bradlc.vscode-tailwindcss",
    "ms-python.python",
    "ms-python.flake8",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

#### Settings.json

```json
{
  "editor.formatOnSave": true,
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "typescript.preferences.includePackageJsonAutoImports": "on"
}
```

## Development Workflows

### Frontend Development

#### Starting Development Server

```bash
cd frontend
npm run dev
```

#### Building for Production

```bash
npm run build
npm start
```

#### Linting and Formatting

```bash
npm run lint
npm run lint:fix
```

#### Component Development

The platform uses a modern component system:

```tsx
import { Button, Card, Badge } from '@/components/ui'

function MyComponent() {
  return (
    <Card variant="elevated" hover>
      <CardContent>
        <Button variant="primary" size="lg">
          Action Button
        </Button>
        <Badge variant="success" dot>
          Active
        </Badge>
      </CardContent>
    </Card>
  )
}
```

### Backend Development

#### Starting Development Server

```bash
cd backend
source venv/bin/activate  # Unix/Linux/macOS
# venv\Scripts\activate   # Windows

uvicorn app.main:app --reload
```

#### Database Operations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

#### Adding New Scanner

```python
# backend/app/scanners/my_scanner.py
from .base import BaseScannerModule, ScannerType

class MyScanner(BaseScannerModule):
    def __init__(self):
        super().__init__(
            name="my_scanner",
            scanner_type=ScannerType.EMAIL,
            description="My custom scanner"
        )
    
    async def scan(self, query):
        # Implementation
        return {"results": "data"}

# Register in implementations.py
from .my_scanner import MyScanner
scanner_registry.register(MyScanner())
```

### Testing

#### Backend Tests

```bash
cd backend
pytest tests/ -v
python -m pytest tests/test_scanners.py
```

#### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

#### Platform Validation

```bash
# Comprehensive platform test
python validate_platform.py

# Expected output: 83.3% readiness (5/6 components)
```

## Production Deployment

### Docker Deployment

#### Development Environment

```bash
docker-compose up -d
```

#### Production Environment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

#### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build
npm run export  # For static deployment
```

#### Backend (VPS/Cloud)

```bash
cd backend
pip install -r requirements.prod.txt
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000

# Kill process on port 8000
npx kill-port 8000
```

#### 2. Python Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf backend/venv
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Node Modules Issues

```bash
# Clean and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 4. Database Issues

```bash
# Reset database
rm backend/intelligence_platform.db
cd backend
alembic upgrade head
```

### Debug Mode

#### Backend Debug

```bash
# Set debug environment
export DEBUG=1
uvicorn app.main:app --reload --log-level debug
```

#### Frontend Debug

```bash
# Enable debug mode
export NODE_ENV=development
export NEXT_PUBLIC_DEBUG=1
npm run dev
```

## Performance Optimization

### Frontend Optimization

1. **Bundle Analysis**
   ```bash
   npm run analyze
   ```

2. **Image Optimization**
   - Use Next.js Image component
   - WebP format for images
   - Proper sizing and lazy loading

3. **Code Splitting**
   - Dynamic imports for heavy components
   - Route-based code splitting

### Backend Optimization

1. **Database Optimization**
   - Proper indexing
   - Connection pooling
   - Query optimization

2. **Caching**
   - Redis for session storage
   - API response caching
   - Static file caching

3. **Monitoring**
   - Health check endpoints
   - Performance metrics
   - Error tracking

## Security Considerations

### Development Security

1. **Environment Variables**
   - Never commit secrets to Git
   - Use strong passwords and keys
   - Rotate credentials regularly

2. **Dependencies**
   - Regular security updates
   - Vulnerability scanning
   - Lock file management

3. **Code Quality**
   - ESLint and Prettier for consistency
   - Pre-commit hooks
   - Code review process

### Production Security

1. **HTTPS Only**
2. **Secure headers**
3. **Rate limiting**
4. **Input validation**
5. **SQL injection prevention**
6. **XSS protection**

## Contributing

### Code Style

1. **Frontend**
   - ESLint + Prettier
   - TypeScript strict mode
   - Tailwind CSS for styling
   - Functional components with hooks

2. **Backend**
   - PEP 8 compliance
   - Type hints required
   - Async/await patterns
   - Comprehensive error handling

### Git Workflow

1. **Branching**
   ```bash
   git checkout -b feature/new-feature
   git checkout -b fix/bug-fix
   ```

2. **Commits**
   ```bash
   git commit -m "feat: add new scanner module"
   git commit -m "fix: resolve database connection issue"
   ```

3. **Pull Requests**
   - Clear description
   - Test coverage
   - Documentation updates

## Resources

### Documentation

- [MODERN_UI_GUIDE.md](./MODERN_UI_GUIDE.md) - Design system documentation
- [README.md](./README.md) - Project overview
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

### External Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)

### Community

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community support and ideas
- **Wiki**: Additional documentation and guides

## Support

For development support:

1. **Check Documentation**: Start with this guide and related docs
2. **Search Issues**: Look for similar problems on GitHub
3. **Create Issue**: Provide detailed reproduction steps
4. **Community**: Ask in discussions for general help

## Version Information

- **Platform Version**: 2.0.0
- **Node.js**: 20.x LTS
- **Python**: 3.12+
- **Next.js**: 14.0.0
- **FastAPI**: 0.104.1
- **React**: 18.2.0

---

**Happy Coding! 🚀**

This guide ensures you can quickly get the Intelligence Gathering Platform running in your development environment and contribute effectively to the project.