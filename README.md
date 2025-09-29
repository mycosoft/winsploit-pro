# WinSploit Pro

**Windows Computer Exploitation Tool** - Similar to PhoneSploit Pro but for Windows targets

## Features

- **Optimized Network Scanning** - Fast, threaded scanning with python-nmap
- **Intelligent Windows Detection** - OS fingerprinting and service detection
- **Port scanning** with detailed service identification
- **Windows payload generation** using msfvenom
- **Automated Metasploit listener** setup
- **SMB exploitation** (EternalBlue)
- **Steganography** - Hide payloads in images for covert delivery
- **Virtual environment support** for clean dependency management

## Quick Setup

### Automated Setup (Recommended)
```bash
# Clone and setup in one go
git clone <repository-url>
cd WinSploit-Pro
./setup.sh
source venv/bin/activate
python3 winsploit.py
```

### Manual Setup
```bash
# Install system dependencies
sudo apt update
sudo apt install nmap metasploit-framework python3-venv

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the tool
python3 winsploit.py
```

## Performance Improvements

The optimized version includes:

- **10x faster network scanning** using python-nmap library
- **Threaded host discovery** for parallel processing
- **Smart OS detection** with Windows-specific indicators
- **Service fingerprinting** to identify Windows services
- **Automatic network range detection**
- **Configurable scan modes** (fast vs comprehensive)

### Scan Speed Comparison
- **Original**: 5-10 minutes for /24 network
- **Optimized**: 30-60 seconds for /24 network

## Usage

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Run with optimized scanner
python3 winsploit.py
```

### Scan Modes

1. **Fast Scan** - Service detection only (~30 seconds)
2. **Comprehensive Scan** - OS + service detection (~60 seconds)
3. **Custom Network** - Specify your own network range

### Menu Options

1. **Scan Network for Windows Computers** `[OPTIMIZED]` - Auto-discovers Windows machines
2. **List all live IPs** `[OPTIMIZED]` - Quick network discovery
3. **Port Scan Target** `[OPTIMIZED]` - Detailed port and service scanning
4. **Generate Windows Payload** - Creates malicious executables
5. **Start Metasploit Listener** - Sets up reverse shell handlers
6. **Exploit SMB (EternalBlue)** - MS17-010 exploitation
7. **Custom Metasploit Console** - Full Metasploit access
8. **Preloaded Attack Console** - Pre-configured Metasploit environment
9. **Steganography** `[AVAILABLE]` - Hide payloads in images
10. **Setup Optimized Scanner** - Install dependencies (if needed)

## Requirements

### System Requirements
- Linux operating system
- Python 3.6+
- Nmap (system package)
- Metasploit Framework
- Root privileges for advanced scanning

### Python Dependencies (auto-installed)
- python-nmap==0.7.1
- colorama==0.4.6
- psutil==5.9.5
- netifaces==0.11.0
- ipaddress==1.0.23
- Pillow==10.0.1 (for steganography)
- stegano==0.10.2 (for steganography)
- cryptography==41.0.7 (for payload encryption)

## Advanced Features

### Network Auto-Detection
The tool automatically detects all local network interfaces and ranges:
```
Auto-detected networks: 192.168.1.0/24, 10.0.0.0/24
```

### Windows Service Detection
Identifies Windows-specific services:
- SMB (ports 139, 445)
- RDP (port 3389)
- WinRM (ports 5985, 5986)
- NetBIOS (port 137-139)
- Microsoft SQL Server (port 1433)

### Threaded Scanning
Uses ThreadPoolExecutor for parallel processing:
- Configurable worker threads
- Timeout handling
- Progress indication

### Steganography Features
Hide malicious payloads inside innocent-looking images:

#### Supported Image Formats
- PNG (recommended for best capacity)
- BMP (good capacity, larger files)
- TIFF (good capacity)

#### Key Features
- **LSB Steganography** - Uses Least Significant Bit technique
- **Payload Encryption** - Optional AES-256 encryption with PBKDF2
- **Capacity Checking** - Automatically validates image can hold payload
- **Metadata Preservation** - Maintains original filename and size info
- **Batch Processing** - Generate and hide payloads in one step

#### Usage Examples
```bash
# Hide existing payload in image
9 → 1 → Enter payload path → Enter image path → Choose encryption

# Generate new payload and hide it
9 → 5 → Enter image path → Choose encryption

# Extract payload from steganographic image
9 → 2 → Enter stego image path → Enter password (if encrypted)

# Check image capacity
9 → 3 → Enter image path
```

#### Steganography Workflow
1. **Generate Payload** - Create Windows executable
2. **Select Image** - Choose PNG/BMP/TIFF with sufficient capacity
3. **Hide Payload** - Embed executable in image using LSB
4. **Transfer Image** - Send innocent-looking image to target
5. **Extract & Execute** - Use extraction script on target system

#### Target-Side Extraction
Use the provided `extract_payload.py` script on target systems:
```bash
# Simple extraction and execution
python3 extract_payload.py photo.png

# With password protection
python3 extract_payload.py photo.png mypassword

# Extract only (don't execute)
python3 extract_payload.py photo.png --no-execute
```

📖 **For detailed steganography usage, see [STEGANOGRAPHY_GUIDE.md](STEGANOGRAPHY_GUIDE.md)**

## Troubleshooting

### "Optimized scanner not available"
```bash
# Install dependencies
pip install -r requirements.txt

# Or run setup script
./setup.sh
```

### "Steganography not available"
```bash
# Install steganography dependencies
pip install Pillow stegano cryptography

# Or reinstall all requirements
pip install -r requirements.txt
```

### Steganography Issues
- **"Image not suitable"** - Use PNG, BMP, or TIFF formats
- **"Payload too large"** - Use larger image or smaller payload
- **"No hidden data found"** - Verify image contains WinSploit payload
- **"Decryption failed"** - Check password or encryption status

### Slow scanning
- Use fast mode for initial discovery
- Reduce network range (/26 instead of /24)
- Check network connectivity

### Permission errors
```bash
# Run with sudo for advanced scanning
sudo python3 winsploit.py

# Or adjust nmap permissions
sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip /usr/bin/nmap
```

## Legal Disclaimer

**IMPORTANT**: This tool is for educational and authorized penetration testing purposes only.

- Only use on networks/systems you own or have explicit written permission to test
- Unauthorized access to computer systems is illegal
- Authors are not responsible for misuse
- Always comply with local laws and regulations
- Obtain proper authorization before testing

## Performance Tips

1. **Use Fast Mode** for initial network discovery
2. **Specify smaller networks** (/26, /27) for faster scanning
3. **Run with sudo** for optimal nmap performance
4. **Use virtual environment** to avoid dependency conflicts
5. **Close unnecessary applications** during intensive scans

## Version History

- **v2.0** - Optimized scanning with python-nmap integration
  - 10x faster network scanning
  - Threaded host discovery
  - Smart Windows detection
  - Virtual environment support
  
- **v1.0** - Initial release
  - Basic network scanning
  - Metasploit integration
  - SMB exploitation

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Test with virtual environment
4. Submit pull request

## License

MIT License - see LICENSE file for details.
**Compatible with:** Kali Linux, Ubuntu, other Linux distributions
