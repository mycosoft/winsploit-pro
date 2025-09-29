#!/usr/bin/env python3
"""
WinSploit Pro Installation Verification Script
Checks all components and dependencies
"""

import sys
import os
from pathlib import Path

def print_status(message, status):
    """Print status with colored output"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def check_dependencies():
    """Check all Python dependencies"""
    print("🔍 Checking Python Dependencies...")
    
    dependencies = [
        ("nmap", "python-nmap"),
        ("colorama", "colorama"),
        ("psutil", "psutil"),
        ("netifaces", "netifaces"),
        ("PIL", "Pillow"),
        ("stegano.lsb", "stegano"),
        ("cryptography.fernet", "cryptography")
    ]
    
    all_good = True
    for module, package in dependencies:
        try:
            __import__(module)
            print_status(f"{package} imported successfully", True)
        except ImportError:
            print_status(f"{package} import failed", False)
            all_good = False
    
    return all_good

def check_winsploit_modules():
    """Check WinSploit Pro specific modules"""
    print("\n🔍 Checking WinSploit Pro Modules...")
    
    modules = [
        ("network_scanner", "OptimizedNetworkScanner"),
        ("steganography", "SteganographyManager")
    ]
    
    all_good = True
    for module, description in modules:
        try:
            __import__(module)
            print_status(f"{description} available", True)
        except ImportError as e:
            print_status(f"{description} not available: {str(e)}", False)
            all_good = False
    
    return all_good

def check_files():
    """Check required files exist"""
    print("\n🔍 Checking Required Files...")
    
    required_files = [
        "winsploit.py",
        "steganography.py",
        "network_scanner.py",
        "extract_payload.py",
        "stego_utils.py",
        "create_test_image.py",
        "requirements.txt",
        "setup.sh",
        "activate_and_run.sh",
        "README.md",
        "STEGANOGRAPHY_GUIDE.md",
        "QUICK_START.md"
    ]
    
    all_good = True
    for file in required_files:
        exists = Path(file).exists()
        print_status(f"{file} exists", exists)
        if not exists:
            all_good = False
    
    return all_good

def check_test_images():
    """Check test images exist"""
    print("\n🔍 Checking Test Images...")
    
    test_images = [
        "small_test.png",
        "medium_test.png", 
        "large_test.png"
    ]
    
    all_good = True
    for image in test_images:
        exists = Path(image).exists()
        print_status(f"{image} exists", exists)
        if not exists:
            all_good = False
    
    return all_good

def test_steganography():
    """Test steganography functionality"""
    print("\n🔍 Testing Steganography Functionality...")
    
    try:
        from steganography import SteganographyManager
        stego = SteganographyManager()
        
        print_status("SteganographyManager initialized", True)
        print_status(f"Supported formats: {stego.supported_formats}", True)
        
        # Test with a test image if available
        if Path("medium_test.png").exists():
            capacity = stego.get_image_capacity("medium_test.png")
            print_status(f"Image capacity calculation works: {capacity} bytes", capacity > 0)
            return True
        else:
            print_status("No test image available for capacity test", False)
            return False
            
    except Exception as e:
        print_status(f"Steganography test failed: {str(e)}", False)
        return False

def main():
    """Main verification function"""
    print("🚀 WinSploit Pro Installation Verification")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("❌ Python 3.6+ required")
        return False
    
    # Run all checks
    checks = [
        check_dependencies(),
        check_winsploit_modules(),
        check_files(),
        check_test_images(),
        test_steganography()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 ALL CHECKS PASSED!")
        print("✅ WinSploit Pro is ready to use with steganography features")
        print("\n🚀 To start: ./activate_and_run.sh")
        return True
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please review the errors above and fix any issues.")
        
        print("\n🔧 Common fixes:")
        print("- Missing dependencies: pip install -r requirements.txt")
        print("- Missing test images: python create_test_image.py")
        print("- Permission issues: chmod +x *.sh")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
