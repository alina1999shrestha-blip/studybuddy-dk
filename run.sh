#!/bin/bash
# StudyBuddy DK — Run Full Stack

echo "=================================================="
echo "  🚀 StudyBuddy DK — Full Stack Launcher"
echo "=================================================="
echo ""
echo "Starting both FastAPI backend and Streamlit frontend..."
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Start FastAPI in background
echo "📡 Starting FastAPI backend on http://127.0.0.1:8000..."
python api.py &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 3

# Start Streamlit
echo "🎨 Starting Streamlit frontend on http://127.0.0.1:8501..."
streamlit run app.py

# Kill FastAPI when Streamlit exits
kill $FASTAPI_PID 2>/dev/null

echo ""
echo "=================================================="
echo "  ✅ StudyBuddy DK Stopped"
echo "=================================================="
