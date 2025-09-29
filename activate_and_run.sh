#!/bin/bash

echo "🚀 WinSploit Pro - Activation Script"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "winsploit.py" ]; then
    echo "❌ Error: winsploit.py not found. Please run this script from the WinSploit-Pro directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check Python version
echo "🐍 Python version: $(python --version)"

# Verify dependencies
echo "📦 Checking dependencies..."
python -c "
import sys
try:
    import nmap
    from PIL import Image
    from stegano import lsb
    from cryptography.fernet import Fernet
    from steganography import SteganographyManager
    print('✅ All steganography dependencies available!')
except ImportError as e:
    print('❌ Missing dependency:', str(e))
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Dependency check failed. Please run: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "✅ Environment ready!"
echo "🎯 Starting WinSploit Pro..."
echo ""

# Run WinSploit Pro
python winsploit.py
