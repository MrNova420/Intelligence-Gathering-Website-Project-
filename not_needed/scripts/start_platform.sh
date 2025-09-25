#!/bin/bash
# Start the complete Intelligence Gathering Platform
echo "🚀 Starting Complete Intelligence Gathering Platform..."
echo "This will start both backend and frontend services"
echo ""

# Check if tmux is available for better terminal management
if command -v tmux &> /dev/null; then
    echo "Using tmux for better session management..."
    
    # Create new tmux session
    tmux new-session -d -s intelligence_platform
    
    # Start backend in first window
    tmux send-keys -t intelligence_platform:0 './start_backend.sh' Enter
    
    # Create new window for frontend
    tmux new-window -t intelligence_platform
    tmux send-keys -t intelligence_platform:1 './start_frontend.sh' Enter
    
    echo "✅ Services started in tmux session 'intelligence_platform'"
    echo "📱 Use 'tmux attach -t intelligence_platform' to view services"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📖 API Docs: http://localhost:8000/docs"
    
else
    echo "Starting services in background..."
    echo "Note: Install tmux for better session management"
    
    # Start backend in background
    nohup ./start_backend.sh > backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    echo "Starting frontend..."
    ./start_frontend.sh
fi
