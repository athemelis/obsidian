#!/bin/bash

# Enhanced start script for Combined Obsidian Tools
# This script handles port detection automatically

echo "🚀 Starting Obsidian Tools Suite..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing required packages..."
    pip install flask flask-cors pyyaml
else
    source venv/bin/activate
fi

# Backup reminder
echo "📦 Automatic Backup Protection Enabled"
echo "   Your vault will be automatically backed up before any modifications"
echo "   The 3 most recent backups will be retained"
echo ""
echo "   Default paths:"
echo "   - Vault: /Users/tonythem/Obsidian/tonythem/"
echo "   - Backups: /Users/tonythem/Obsidian/backups/"
echo "   (You can change these in the web interface)"
echo ""

# Clean up any existing config
rm -f server_config.json

# Start the server
echo "🌐 Starting server..."
echo "   The server will automatically find an available port"
echo ""

# Run the server in the background and capture output
python obsidian_tools_server.py &
SERVER_PID=$!

# Wait for server to start and create config file
echo "⏳ Waiting for server to start..."
MAX_WAIT=20
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if [ -f "server_config.json" ]; then
        # Give the server a moment to fully initialize
        sleep 2
        break
    fi
    sleep 1
    WAITED=$((WAITED + 1))
done

# Read the port from config
if [ -f "server_config.json" ]; then
    PORT=$(python3 -c "import json; print(json.load(open('server_config.json'))['port'])")
    echo "✅ Server is running on port $PORT"
    
    # Test if server is responding
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/health" | grep -q "200"; then
        echo "✅ Server is responding correctly"
    else
        echo "⚠️  Server might still be starting..."
    fi
    
    # Wait a moment for the server to be fully ready
    sleep 1
    
    # Open the main menu in browser
    echo "🌍 Opening Obsidian Tools Suite..."
    open "http://localhost:$PORT/"
else
    echo "❌ Server failed to start properly"
    echo "   Check for errors above"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo ""
echo "✅ Application is running!"
echo "   - Main menu: http://localhost:$PORT"
echo "   - Note Query Tool: http://localhost:$PORT/query_tool.html"
echo "   - Search & Replace Tool: http://localhost:$PORT/search_replace_tool.html"
echo ""
echo "Press Ctrl+C to stop the server..."

# Handle cleanup on exit
trap "echo ''; echo 'Stopping server...'; kill $SERVER_PID 2>/dev/null; rm -f server_config.json; echo 'Server stopped.'" EXIT

# Wait for the server process
wait $SERVER_PID