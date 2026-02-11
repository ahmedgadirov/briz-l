#!/bin/bash
set -e

echo "🚀 Starting All-in-One Rasa Container..."

# Function to handle shutdown gracefully
cleanup() {
    echo "🛑 Shutting down all services..."
    kill $(jobs -p) 2>/dev/null || true
    wait
    exit 0
}

trap cleanup SIGTERM SIGINT

# Start Rasa Action Server in background
echo "📦 Starting Rasa Action Server on port 5055..."
cd /app
rasa run actions --actions actions --port 5055 &
ACTION_PID=$!

# Wait for action server to be ready
echo "⏳ Waiting for Action Server to start..."
sleep 5

# Start Rasa Server in background
echo "🤖 Starting Rasa Server on port 3000..."
rasa run --enable-api --cors "*" -p 3000 --log-config-file logging.yml &
RASA_PID=$!

# Wait for Rasa to be ready
echo "⏳ Waiting for Rasa Server to start..."
sleep 10

# Start Telegram Poller in foreground
echo "📱 Starting Telegram Poller..."
python telegram_poller.py &
TELEGRAM_PID=$!

echo "✅ All services started!"
echo "   - Action Server: PID $ACTION_PID (port 5055)"
echo "   - Rasa Server: PID $RASA_PID (port 3000)"
echo "   - Telegram Poller: PID $TELEGRAM_PID"
echo ""
echo "📊 Monitoring services..."

# Wait for any process to exit
wait -n

# If any process dies, kill the others and exit
echo "⚠️  A service has stopped. Shutting down..."
cleanup
