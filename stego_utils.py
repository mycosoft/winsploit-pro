#!/usr/bin/env python3
"""
Steganography Utilities for WinSploit Pro
Standalone utilities for steganography operations
"""

import os
import sys
import argparse
from steganography import SteganographyManager

def hide_payload(args):
    """Hide payload in image"""
    stego = SteganographyManager()
    
    if not os.path.exists(args.payload):
        print(f"Error: Payload file not found: {args.payload}")
        return False
    
    if not stego.validate_image(args.image):
        print(f"Error: Invalid or unsuitable image: {args.image}")
        return False
    
    # Check capacity
    capacity = stego.get_image_capacity(args.image)
    payload_size = os.path.getsize(args.payload)
    
    print(f"Image capacity: {capacity} bytes ({capacity/1024:.1f} KB)")
    print(f"Payload size: {payload_size} bytes ({payload_size/1024:.1f} KB)")
    
    if payload_size > capacity:
        print("Error: Payload too large for this image")
        return False
    
    # Hide payload
    success = stego.hide_payload_in_image(
        args.payload, 
        args.image, 
        args.output, 
        args.password
    )
    
    if success:
        print(f"Success: Payload hidden in {args.output}")
        return True
    else:
        print("Error: Failed to hide payload")
        return False

def extract_payload(args):
    """Extract payload from image"""
    stego = SteganographyManager()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        return False
    
    success = stego.extract_payload_from_image(
        args.image,
        args.output,
        args.password
    )
    
    if success:
        print(f"Success: Payload extracted to {args.output}")
        return True
    else:
        print("Error: Failed to extract payload")
        return False

def check_capacity(args):
    """Check image capacity"""
    stego = SteganographyManager()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        return False
    
    if not stego.validate_image(args.image):
        print(f"Error: Image not suitable for steganography")
        print("Supported formats: PNG, BMP, TIFF")
        return False
    
    capacity = stego.get_image_capacity(args.image)
    print(f"Image: {args.image}")
    print(f"Capacity: {capacity} bytes ({capacity/1024:.1f} KB)")
    
    # Show payload size comparisons
    print("\nPayload size reference:")
    print(f"- Small payload (~50 KB): {'✓' if capacity >= 50*1024 else '✗'}")
    print(f"- Medium payload (~200 KB): {'✓' if capacity >= 200*1024 else '✗'}")
    print(f"- Large payload (~1 MB): {'✓' if capacity >= 1024*1024 else '✗'}")
    
    return True

def list_images(args):
    """List suitable images in directory"""
    stego = SteganographyManager()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        return False
    
    images = stego.list_suitable_images(args.directory)
    
    if not images:
        print(f"No suitable images found in {args.directory}")
        return False
    
    print(f"Suitable images in {args.directory}:")
    print("-" * 60)
    for i, img in enumerate(images, 1):
        print(f"{i:2d}. {img['filename']:<30} {img['capacity']/1024:>8.1f} KB")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="WinSploit Pro Steganography Utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Hide payload in image
  python3 stego_utils.py hide payload.exe photo.png output.png
  
  # Hide with encryption
  python3 stego_utils.py hide payload.exe photo.png output.png -p mypassword
  
  # Extract payload
  python3 stego_utils.py extract stego.png extracted.exe
  
  # Extract with password
  python3 stego_utils.py extract stego.png extracted.exe -p mypassword
  
  # Check image capacity
  python3 stego_utils.py capacity photo.png
  
  # List suitable images
  python3 stego_utils.py list /path/to/images/
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Hide command
    hide_parser = subparsers.add_parser('hide', help='Hide payload in image')
    hide_parser.add_argument('payload', help='Path to payload file')
    hide_parser.add_argument('image', help='Path to cover image')
    hide_parser.add_argument('output', help='Path for output steganographic image')
    hide_parser.add_argument('-p', '--password', help='Encryption password')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract payload from image')
    extract_parser.add_argument('image', help='Path to steganographic image')
    extract_parser.add_argument('output', help='Path for extracted payload')
    extract_parser.add_argument('-p', '--password', help='Decryption password')
    
    # Capacity command
    capacity_parser = subparsers.add_parser('capacity', help='Check image capacity')
    capacity_parser.add_argument('image', help='Path to image file')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List suitable images')
    list_parser.add_argument('directory', help='Directory to search')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'hide':
        success = hide_payload(args)
    elif args.command == 'extract':
        success = extract_payload(args)
    elif args.command == 'capacity':
        success = check_capacity(args)
    elif args.command == 'list':
        success = list_images(args)
    else:
        parser.print_help()
        return
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
