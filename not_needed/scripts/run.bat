@echo off
REM 🚀 Windows Batch Script for Intelligence Gathering Platform
REM This works on Windows with Python and Node.js installed

echo 🚀 Intelligence Gathering Platform - Windows Setup
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Python and Node.js found!

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd backend
pip install -r requirements-lite.txt --user --quiet || pip install fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] --user --quiet
cd ..

REM Setup environment
if not exist .env (
    echo 🔧 Setting up environment...
    if exist .env.example (
        copy .env.example .env >nul
    ) else (
        echo DATABASE_URL=sqlite:///./intelligence_platform.db > .env
        echo SECRET_KEY=windows-dev-key >> .env
        echo DEBUG=true >> .env
        echo ENVIRONMENT=windows >> .env
    )
)

REM Setup database
echo 🗄️ Setting up database...
cd backend
python app/db/setup_standalone.py
cd ..

REM Install Node.js dependencies
if exist frontend (
    echo 📦 Installing Node.js dependencies...
    cd frontend
    npm install --silent
    cd ..
)

REM Start services
echo 🚀 Starting services...
echo.
echo 🌐 Access Points:
echo    • Backend API: http://localhost:8000
echo    • API Docs: http://localhost:8000/docs
if exist frontend (
    echo    • Frontend Website: http://localhost:3000
)
echo.
echo 💡 Press Ctrl+C to stop the services
echo.

REM Start backend in background
cd backend
start /b python run_standalone.py
cd ..

REM Start frontend if exists
if exist frontend (
    cd frontend
    start /b npm run dev
    cd ..
)

echo ✅ Services started! Check the URLs above.
echo Press any key to stop all services...
pause >nul

REM Stop services
echo 🛑 Stopping services...
taskkill /f /im python.exe /fi "windowtitle eq run_standalone.py*" >nul 2>&1
taskkill /f /im node.exe /fi "windowtitle eq npm*" >nul 2>&1

echo ✅ All services stopped.
pause