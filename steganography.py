#!/usr/bin/env python3
"""
Steganography Module for WinSploit Pro
Handles hiding and extracting payloads in/from images
"""

import os
import base64
import hashlib
from PIL import Image
from stegano import lsb
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SteganographyManager:
    def __init__(self):
        self.supported_formats = ['.png', '.bmp', '.tiff']
        
    def generate_key_from_password(self, password: str, salt: bytes = None) -> tuple:
        """Generate encryption key from password"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_payload(self, payload_data: bytes, password: str) -> tuple:
        """Encrypt payload data with password"""
        key, salt = self.generate_key_from_password(password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(payload_data)
        return encrypted_data, salt
    
    def decrypt_payload(self, encrypted_data: bytes, password: str, salt: bytes) -> bytes:
        """Decrypt payload data with password"""
        key, _ = self.generate_key_from_password(password, salt)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data
    
    def validate_image(self, image_path: str) -> bool:
        """Validate if image is suitable for steganography"""
        if not os.path.exists(image_path):
            return False
        
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in self.supported_formats:
            return False
        
        try:
            with Image.open(image_path) as img:
                # Check if image is large enough
                if img.width * img.height < 10000:  # Minimum 100x100 pixels
                    return False
                return True
        except Exception:
            return False
    
    def hide_payload_in_image(self, payload_path: str, image_path: str, output_path: str, password: str = None) -> bool:
        """Hide payload in image using LSB steganography"""
        try:
            # Validate inputs
            if not os.path.exists(payload_path):
                print(f"Payload file not found: {payload_path}")
                return False
            
            if not self.validate_image(image_path):
                print(f"Invalid or unsuitable image: {image_path}")
                return False
            
            # Read payload
            with open(payload_path, 'rb') as f:
                payload_data = f.read()
            
            # Encrypt payload if password provided
            if password:
                encrypted_payload, salt = self.encrypt_payload(payload_data, password)
                # Prepend salt to encrypted data
                data_to_hide = salt + b'|ENCRYPTED|' + encrypted_payload
            else:
                data_to_hide = b'|PLAIN|' + payload_data
            
            # Encode data as base64 for text-based hiding
            encoded_data = base64.b64encode(data_to_hide).decode('utf-8')
            
            # Add metadata
            payload_name = os.path.basename(payload_path)
            metadata = f"WINSPLOIT_PAYLOAD:{payload_name}:{len(payload_data)}:"
            final_data = metadata + encoded_data
            
            # Hide data in image
            secret_image = lsb.hide(image_path, final_data)
            secret_image.save(output_path)
            
            print(f"Payload successfully hidden in: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error hiding payload: {e}")
            return False
    
    def extract_payload_from_image(self, image_path: str, output_path: str, password: str = None) -> bool:
        """Extract payload from image"""
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
                payload_data = self.decrypt_payload(encrypted_payload, password, salt)
                
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
            with open(output_path, 'wb') as f:
                f.write(payload_data)
            
            print(f"Payload extracted successfully: {output_path}")
            print(f"Original filename: {payload_name}")
            print(f"Payload size: {payload_size} bytes")
            return True
            
        except Exception as e:
            print(f"Error extracting payload: {e}")
            return False
    
    def get_image_capacity(self, image_path: str) -> int:
        """Calculate maximum payload size that can be hidden in image"""
        try:
            with Image.open(image_path) as img:
                # LSB can hide 1 bit per pixel per channel
                # For RGB images, that's 3 bits per pixel
                # Convert to bytes and account for overhead
                total_pixels = img.width * img.height
                if img.mode == 'RGB':
                    capacity_bits = total_pixels * 3
                elif img.mode == 'RGBA':
                    capacity_bits = total_pixels * 4
                else:
                    capacity_bits = total_pixels
                
                # Convert to bytes and subtract overhead for metadata
                capacity_bytes = (capacity_bits // 8) - 1000  # 1KB overhead
                return max(0, capacity_bytes)
        except Exception:
            return 0
    
    def list_suitable_images(self, directory: str) -> list:
        """List images suitable for steganography in directory"""
        suitable_images = []
        
        if not os.path.exists(directory):
            return suitable_images
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and self.validate_image(filepath):
                capacity = self.get_image_capacity(filepath)
                suitable_images.append({
                    'path': filepath,
                    'filename': filename,
                    'capacity': capacity
                })
        
        return suitable_images
