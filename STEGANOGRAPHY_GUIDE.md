# WinSploit Pro - Steganography Guide

## Overview

The steganography feature in WinSploit Pro allows you to hide malicious payloads inside innocent-looking images. This technique is useful for covert payload delivery, bypassing basic security measures, and social engineering attacks.

## Quick Start

### 1. Generate Test Images
```bash
# Create test images for practice
python3 create_test_image.py
```

### 2. Basic Workflow
```bash
# Run WinSploit Pro
python3 winsploit.py

# Select steganography menu (option 9)
# Choose "Generate Payload + Hide in Image" (option 5)
# Follow the prompts
```

## Detailed Usage

### Menu Option 9: Steganography

#### Sub-menu Options:
1. **Hide Payload in Image** - Hide existing payload in image
2. **Extract Payload from Image** - Extract hidden payload
3. **Check Image Capacity** - Verify image can hold payload
4. **List Suitable Images** - Find compatible images in directory
5. **Generate Payload + Hide in Image** - Complete workflow

### Supported Image Formats

| Format | Capacity | File Size | Recommendation |
|--------|----------|-----------|----------------|
| PNG    | High     | Medium    | **Best choice** - good compression, high capacity |
| BMP    | Highest  | Large     | Maximum capacity but large files |
| TIFF   | High     | Medium    | Good alternative to PNG |

❌ **Not Supported:** JPG, GIF, WebP (lossy compression destroys hidden data)

### Image Capacity Guidelines

| Image Size | Estimated Capacity | Suitable For |
|------------|-------------------|--------------|
| 400x300    | ~35 KB           | Small payloads |
| 800x600    | ~140 KB          | Medium payloads |
| 1200x900   | ~320 KB          | Large payloads |
| 1920x1080  | ~620 KB          | Very large payloads |

**Formula:** Capacity ≈ (Width × Height × 3) ÷ 8 - 1KB overhead

## Step-by-Step Tutorials

### Tutorial 1: Hide Existing Payload

1. **Prepare payload:**
   ```bash
   # Generate payload first (option 4 in main menu)
   # Or use existing executable
   ```

2. **Select image:**
   - Use PNG, BMP, or TIFF format
   - Ensure image is large enough for payload
   - Check capacity with option 3

3. **Hide payload:**
   ```
   Main Menu → 9 (Steganography) → 1 (Hide Payload)
   Enter payload path: payloads/windows_payload_20231201_143022.exe
   Enter image path: test_images/medium_test.png
   Image capacity: 143360 bytes
   Payload size: 73802 bytes
   Enter output image path: stego_medium_test.png
   Encrypt payload? (y/N): y
   Enter encryption password: mySecretPassword123
   ```

### Tutorial 2: Generate and Hide in One Step

```
Main Menu → 9 (Steganography) → 5 (Generate Payload + Hide)
[Payload generation process...]
Payload generated: payloads/windows_payload_20231201_143525.exe
Enter image path: test_images/large_test.png
[Capacity check passes...]
Enter output image path: vacation_photo.png
Encrypt payload? (y/N): y
Enter encryption password: familyTrip2023
```

### Tutorial 3: Extract Payload on Target

**Method 1: Using extract_payload.py**
```bash
# Copy extract_payload.py to target system
# Transfer steganographic image to target

# Extract and execute
python3 extract_payload.py vacation_photo.png familyTrip2023

# Extract only (don't execute)
python3 extract_payload.py vacation_photo.png familyTrip2023 --no-execute
```

**Method 2: Using WinSploit Pro**
```
Main Menu → 9 (Steganography) → 2 (Extract Payload)
Enter steganographic image path: vacation_photo.png
Enter output payload path: extracted_payload.exe
Is payload encrypted? (y/N): y
Enter decryption password: familyTrip2023
```

## Command Line Utilities

### stego_utils.py - Advanced Operations

```bash
# Hide payload with encryption
python3 stego_utils.py hide payload.exe photo.png output.png -p password123

# Extract payload
python3 stego_utils.py extract stego.png extracted.exe -p password123

# Check image capacity
python3 stego_utils.py capacity photo.png

# List suitable images in directory
python3 stego_utils.py list /home/user/Pictures/
```

## Security Considerations

### Encryption Best Practices
- **Always use encryption** for sensitive payloads
- **Use strong passwords** (12+ characters, mixed case, numbers, symbols)
- **Don't reuse passwords** across different operations
- **Consider password complexity** vs target user capability

### Operational Security
- **Choose realistic cover images** (vacation photos, memes, etc.)
- **Maintain original image metadata** when possible
- **Use appropriate file names** (avoid suspicious names)
- **Test extraction** before deploying to targets
- **Have backup delivery methods** in case steganography fails

### Detection Evasion
- **Avoid obvious patterns** in image selection
- **Use images with natural noise** (photos vs computer graphics)
- **Don't modify image dimensions** unnecessarily
- **Keep file sizes reasonable** for the context

## Troubleshooting

### Common Issues

#### "Image not suitable for steganography"
- **Cause:** Wrong format (JPG, GIF) or corrupted image
- **Solution:** Convert to PNG/BMP/TIFF or use different image

#### "Payload too large for this image"
- **Cause:** Image capacity insufficient
- **Solution:** Use larger image or compress payload

#### "No hidden data found in image"
- **Cause:** Image doesn't contain WinSploit payload or corrupted
- **Solution:** Verify correct steganographic image

#### "Decryption failed"
- **Cause:** Wrong password or payload not encrypted
- **Solution:** Check password and encryption status

#### "Module not found" errors
- **Cause:** Missing steganography dependencies
- **Solution:** 
  ```bash
  pip install Pillow stegano cryptography
  # or
  pip install -r requirements.txt
  ```

### Performance Tips

1. **Use PNG format** for best balance of capacity and file size
2. **Pre-check capacity** before attempting to hide large payloads
3. **Use compression** on payloads when possible (UPX, etc.)
4. **Batch process** multiple payloads with scripting

## Advanced Techniques

### Custom Image Preparation
```python
# Create optimal steganography image
from PIL import Image
import numpy as np

# Create image with maximum entropy (random noise)
width, height = 1200, 900
noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
img = Image.fromarray(noise)
img.save('optimal_stego_base.png')
```

### Batch Operations
```bash
# Hide multiple payloads
for payload in payloads/*.exe; do
    python3 stego_utils.py hide "$payload" base_image.png "stego_$(basename $payload .exe).png" -p password123
done
```

### Integration with Social Engineering
1. **Use contextually appropriate images** (company logos, event photos)
2. **Maintain consistent metadata** (camera info, timestamps)
3. **Test with target's typical image viewers**
4. **Consider file size limitations** of delivery methods (email, messaging)

## Legal and Ethical Guidelines

⚠️ **IMPORTANT DISCLAIMERS:**

- **Only use on authorized targets** with explicit written permission
- **Comply with local laws** regarding penetration testing
- **Document all activities** for legitimate security assessments
- **Obtain proper authorization** before testing
- **Respect privacy and data protection** laws

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research and education
- ✅ Red team exercises with permission
- ✅ Personal learning environments

This tool is NOT for:
- ❌ Unauthorized access to systems
- ❌ Malicious attacks
- ❌ Privacy violations
- ❌ Illegal activities

## Support and Resources

### Getting Help
- Check troubleshooting section above
- Review error messages carefully
- Test with provided sample images
- Verify all dependencies are installed

### Additional Resources
- [Steganography Theory](https://en.wikipedia.org/wiki/Steganography)
- [LSB Steganography Explanation](https://www.geeksforgeeks.org/lsb-based-image-steganography-using-matlab/)
- [Digital Forensics Detection Methods](https://resources.infosecinstitute.com/topic/steganography-and-tools-to-perform-steganography/)

---

**Remember:** With great power comes great responsibility. Use these capabilities ethically and legally.
