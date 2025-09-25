#!/bin/bash
# 🚀 Super Simple Run Script - Just run this and everything works!
# Perfect for users who want zero configuration

echo "🚀 Starting Intelligence Gathering Platform..."
echo "This will handle everything automatically!"
echo ""

# Make sure easy_start.sh is executable
chmod +x easy_start.sh

# Check if this is first run
if [[ ! -f ".env" ]] || [[ ! -f "backend/intelligence_platform.db" ]]; then
    echo "🔧 First time setup detected..."
    ./easy_start.sh setup
    echo ""
    echo "✅ Setup complete! Starting services..."
    ./easy_start.sh start
else
    echo "🚀 Starting services..."
    ./easy_start.sh start
fi

echo ""
echo "🎉 Platform is running!"
echo ""
echo "🌐 Access your platform at:"
echo "   • Website: http://localhost:3000"
echo "   • API: http://localhost:8000"
echo ""
echo "💡 Useful commands:"
echo "   • Stop: ./easy_start.sh stop"
echo "   • Restart: ./easy_start.sh restart"
echo "   • Status: ./easy_start.sh status"