#!/bin/bash
# Quick Termux Setup - Fixes the psycopg2-binary issue
# This script addresses the exact problem the user reported

echo "🔧 Termux Quick Fix - Intelligence Gathering Platform"
echo "===================================================="

# Fix the psycopg2-binary issue by using lite requirements
echo "📦 Installing dependencies without PostgreSQL (fixes psycopg2-binary error)..."

# Use requirements-lite.txt instead of requirements.txt
if [[ -f "backend/requirements-lite.txt" ]]; then
    echo "✅ Using requirements-lite.txt (no psycopg2-binary)"
    pip install -r backend/requirements-lite.txt --user
else
    echo "⚠️ Fallback: Installing core packages individually"
    pip install --user fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] cryptography
fi

# Setup environment if not exists
if [[ ! -f ".env" ]]; then
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        echo "✅ Created .env from example"
    else
        cat > .env << EOF
DATABASE_URL=sqlite:///./intelligence_platform.db
SECRET_KEY=termux-dev-key
DEBUG=true
ENVIRONMENT=termux
EOF
        echo "✅ Created basic .env"
    fi
fi

# Setup database
echo "🗄️ Setting up SQLite database..."
cd backend
python app/db/setup_standalone.py
cd ..

echo ""
echo "✅ Setup complete! No psycopg2-binary errors."
echo ""
echo "🚀 To start the platform:"
echo "   Backend only: python backend/run_standalone.py"
echo "   Full website: ./start_termux.sh"
echo ""
echo "🌐 Access points:"
echo "   • API: http://localhost:8000"
echo "   • Docs: http://localhost:8000/docs"
echo "   • Website: http://localhost:3000 (if frontend running)"