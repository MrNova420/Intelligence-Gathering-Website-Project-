#!/bin/bash
# Start the Intelligence Gathering Platform Backend
echo "🚀 Starting Intelligence Gathering Platform Backend..."
cd backend

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Start the server
echo "🌐 Backend will be available at http://localhost:8000"
echo "📖 API documentation at http://localhost:8000/docs"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
