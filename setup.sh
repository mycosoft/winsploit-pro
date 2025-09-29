#!/bin/bash

echo "Setting up WinSploit Pro environment..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if nmap is installed on system
if ! command -v nmap &> /dev/null; then
    echo "WARNING: nmap is not installed on your system."
    echo "Please install nmap using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install nmap"
    echo "  CentOS/RHEL: sudo yum install nmap"
    echo "  Arch: sudo pacman -S nmap"
fi

# Check if metasploit is installed
if ! command -v msfconsole &> /dev/null; then
    echo "WARNING: Metasploit Framework is not installed."
    echo "Please install Metasploit Framework for full functionality."
fi

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To run WinSploit Pro: python3 winsploit.py"
