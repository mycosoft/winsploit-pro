#!/usr/bin/env python3
"""
Create test images for steganography testing
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(filename="test_image.png", width=800, height=600):
    """Create a test image suitable for steganography"""
    
    # Create a new image with RGB mode
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Add some visual elements
    # Draw gradient background
    for y in range(height):
        color_val = int(255 * (y / height))
        draw.line([(0, y), (width, y)], fill=(color_val, 200, 255 - color_val))
    
    # Add some geometric shapes
    draw.rectangle([50, 50, 200, 150], fill='red', outline='darkred', width=3)
    draw.ellipse([250, 100, 400, 200], fill='green', outline='darkgreen', width=3)
    draw.polygon([(500, 50), (600, 150), (450, 150)], fill='yellow', outline='orange', width=3)
    
    # Add text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
        draw.text((50, 250), "WinSploit Pro Test Image", fill='black', font=font)
        draw.text((50, 280), "Suitable for steganography testing", fill='darkblue', font=font)
        draw.text((50, 310), f"Resolution: {width}x{height}", fill='darkgreen', font=font)
        
        # Calculate capacity
        capacity = (width * height * 3) // 8 - 1000  # RGB, minus overhead
        draw.text((50, 340), f"Estimated capacity: ~{capacity/1024:.1f} KB", fill='purple', font=font)
        
    except:
        # Fallback if font loading fails
        draw.text((50, 250), "WinSploit Pro Test Image", fill='black')
    
    # Add some noise for better steganography
    import random
    for _ in range(1000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.point((x, y), fill=color)
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Test image created: {filename}")
    print(f"Resolution: {width}x{height}")
    print(f"Estimated capacity: ~{capacity/1024:.1f} KB")
    
    return filename

def create_multiple_test_images():
    """Create multiple test images with different sizes"""
    sizes = [
        (400, 300, "small_test.png"),
        (800, 600, "medium_test.png"),
        (1200, 900, "large_test.png")
    ]
    
    created_images = []
    for width, height, filename in sizes:
        img_path = create_test_image(filename, width, height)
        created_images.append(img_path)
    
    return created_images

if __name__ == "__main__":
    print("Creating test images for steganography...")
    images = create_multiple_test_images()
    print(f"\nCreated {len(images)} test images:")
    for img in images:
        print(f"- {img}")
    print("\nYou can now use these images to test the steganography feature!")
