# WinSploit Pro - Quick Start Guide

## ✅ Environment Setup Complete!

Your WinSploit Pro environment is now fully configured with steganography capabilities.

## 🚀 How to Run

### Option 1: Using the Activation Script (Recommended)
```bash
./activate_and_run.sh
```

### Option 2: Manual Activation
```bash
source venv/bin/activate
python winsploit.py
```

## 🎯 New Steganography Feature

### Main Menu → Option 9: Steganography

**Available Operations:**
1. **Hide Payload in Image** - Hide existing payload in image
2. **Extract Payload from Image** - Extract hidden payload
3. **Check Image Capacity** - Verify image can hold payload
4. **List Suitable Images** - Find compatible images in directory
5. **Generate Payload + Hide in Image** - Complete workflow

### 🖼️ Test Images Available
- `small_test.png` - 43.0 KB capacity
- `medium_test.png` - 174.8 KB capacity  
- `large_test.png` - 394.5 KB capacity

## 🔧 Command Line Tools

### Check Image Capacity
```bash
source venv/bin/activate
python stego_utils.py capacity medium_test.png
```

### List Suitable Images
```bash
source venv/bin/activate
python stego_utils.py list .
```

### Hide Payload (when you have one)
```bash
source venv/bin/activate
python stego_utils.py hide payload.exe medium_test.png output.png -p password123
```

### Extract Payload
```bash
source venv/bin/activate
python stego_utils.py extract output.png extracted.exe -p password123
```

## 📋 Dependencies Status

✅ **All dependencies installed successfully:**
- python-nmap==0.7.1
- colorama==0.4.6
- psutil==5.9.8
- netifaces==0.11.0
- Pillow>=10.2.0 (installed: 11.3.0)
- stegano>=0.10.2 (installed: 2.0.0)
- cryptography>=41.0.0 (installed: 46.0.1)

✅ **Module Status:**
- OptimizedNetworkScanner: Available
- SteganographyManager: Available
- All steganography features: Functional

## 🎮 Quick Test Workflow

1. **Start WinSploit Pro:**
   ```bash
   ./activate_and_run.sh
   ```

2. **Generate a payload:**
   - Choose option 4 (Generate Windows Payload)

3. **Test steganography:**
   - Choose option 9 (Steganography)
   - Choose option 1 (Hide Payload in Image)
   - Use one of the test images (medium_test.png)
   - Try with and without encryption

4. **Extract and verify:**
   - Choose option 2 (Extract Payload from Image)
   - Verify the extracted payload matches the original

## 🔍 Troubleshooting

### If you see "Steganography not available"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### If virtual environment is missing
```bash
./setup.sh
source venv/bin/activate
```

### Check all dependencies
```bash
source venv/bin/activate
python -c "from steganography import SteganographyManager; print('✅ Ready!')"
```

## 📚 Documentation

- **Main Documentation:** `README.md`
- **Detailed Steganography Guide:** `STEGANOGRAPHY_GUIDE.md`
- **This Quick Start:** `QUICK_START.md`

## 🎯 Ready to Use!

Your WinSploit Pro installation is now complete with:
- ✅ Optimized network scanning
- ✅ Windows exploitation capabilities  
- ✅ **NEW: Steganography for covert payload delivery**
- ✅ All dependencies properly installed
- ✅ Test images ready for demonstration

**Start with:** `./activate_and_run.sh`
