#!/bin/bash
# PhonePe Dashboard Startup Script

echo "🚀 PhonePe Analytics Dashboard"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python installed: $(python3 --version)"
echo ""

# Check if in dashboard directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the dashboard directory"
    exit 1
fi

echo "📦 Checking dependencies..."

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ All dependencies ready"
echo ""

# Launch Streamlit
echo "🌐 Launching dashboard at http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

python3 -m streamlit run app.py
