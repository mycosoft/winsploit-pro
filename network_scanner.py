#!/usr/bin/env python3
"""
Optimized Network Scanner Module for WinSploit Pro
Uses python-nmap for faster and more efficient scanning
"""

import nmap
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import netifaces
import ipaddress

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

class OptimizedNetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.windows_indicators = [
            'Windows', 'Microsoft', 'SMB', 'NetBIOS', 'RDP', 'WinRM',
            'microsoft-ds', 'netbios-ssn', 'ms-wbt-server'
        ]
        
    def get_local_networks(self):
        """Get all local network ranges"""
        networks = []
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        netmask = addr_info.get('netmask')
                        if ip and netmask and not ip.startswith('127.'):
                            try:
                                network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                                networks.append(str(network))
                            except:
                                continue
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not enumerate all networks: {e}{Colors.END}")
            # Fallback to basic network detection
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
                networks.append(network)
            except:
                networks.append('192.168.1.0/24')
        
        return networks

    def ping_sweep(self, network, timeout=3):
        """Fast ping sweep to find live hosts"""
        print(f"{Colors.CYAN}Performing ping sweep on {network}...{Colors.END}")
        
        try:
            # Use nmap for ping sweep - much faster than individual pings
            self.nm.scan(hosts=network, arguments=f'-sn -T4 --max-retries 1 --host-timeout {timeout}s')
            
            live_hosts = []
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    live_hosts.append(host)
                    
            print(f"{Colors.GREEN}Found {len(live_hosts)} live hosts{Colors.END}")
            return live_hosts
            
        except Exception as e:
            print(f"{Colors.RED}Ping sweep failed: {e}{Colors.END}")
            return []

    def detect_os_threaded(self, hosts, max_workers=10):
        """Detect OS using threading for faster scanning"""
        print(f"{Colors.CYAN}Detecting operating systems on {len(hosts)} hosts...{Colors.END}")
        
        windows_hosts = []
        
        def scan_host_os(host):
            try:
                # Quick OS detection scan
                self.nm.scan(host, arguments='-O -T4 --max-retries 1 --host-timeout 10s')
                
                if host in self.nm.all_hosts():
                    host_info = self.nm[host]
                    
                    # Check OS detection results
                    if 'osmatch' in host_info:
                        for osmatch in host_info['osmatch']:
                            os_name = osmatch.get('name', '').lower()
                            if any(indicator.lower() in os_name for indicator in self.windows_indicators):
                                return {
                                    'ip': host,
                                    'os': osmatch.get('name', 'Unknown'),
                                    'accuracy': osmatch.get('accuracy', 0)
                                }
                
                return None
                
            except Exception as e:
                print(f"{Colors.YELLOW}OS detection failed for {host}: {e}{Colors.END}")
                return None
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_host = {executor.submit(scan_host_os, host): host for host in hosts}
            
            for future in as_completed(future_to_host):
                result = future.result()
                if result:
                    windows_hosts.append(result)
                    print(f"{Colors.GREEN}Windows host found: {result['ip']} - {result['os']} ({result['accuracy']}% accuracy){Colors.END}")
        
        return windows_hosts

    def service_detection(self, hosts, ports=None, max_workers=5):
        """Detect services that might indicate Windows systems"""
        if ports is None:
            # Common Windows ports
            ports = [135, 139, 445, 3389, 5985, 5986, 1433, 1521, 80, 443, 21, 22, 23, 25, 53, 110, 143, 993, 995, 1723]
        
        print(f"{Colors.CYAN}Scanning services on {len(hosts)} hosts...{Colors.END}")
        
        windows_services = []
        
        def scan_host_services(host):
            try:
                port_list = ','.join(map(str, ports))
                self.nm.scan(host, port_list, arguments='-sV -T4 --max-retries 1 --host-timeout 15s')
                
                if host in self.nm.all_hosts():
                    host_info = self.nm[host]
                    windows_indicators_found = []
                    
                    for protocol in host_info.all_protocols():
                        ports_info = host_info[protocol].keys()
                        for port in ports_info:
                            port_info = host_info[protocol][port]
                            service = port_info.get('name', '')
                            product = port_info.get('product', '')
                            version = port_info.get('version', '')
                            
                            # Check for Windows-specific services
                            if (port in [135, 139, 445] or  # SMB/NetBIOS
                                port == 3389 or  # RDP
                                port in [5985, 5986] or  # WinRM
                                'microsoft' in product.lower() or
                                'windows' in product.lower() or
                                service in ['microsoft-ds', 'netbios-ssn', 'ms-wbt-server']):
                                
                                windows_indicators_found.append({
                                    'port': port,
                                    'service': service,
                                    'product': product,
                                    'version': version
                                })
                    
                    if windows_indicators_found:
                        return {
                            'ip': host,
                            'services': windows_indicators_found
                        }
                
                return None
                
            except Exception as e:
                print(f"{Colors.YELLOW}Service scan failed for {host}: {e}{Colors.END}")
                return None
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_host = {executor.submit(scan_host_services, host): host for host in hosts}
            
            for future in as_completed(future_to_host):
                result = future.result()
                if result:
                    windows_services.append(result)
                    print(f"{Colors.GREEN}Windows services found on {result['ip']}:{Colors.END}")
                    for service in result['services']:
                        print(f"  {Colors.YELLOW}Port {service['port']}: {service['service']} ({service['product']} {service['version']}){Colors.END}")
        
        return windows_services

    def comprehensive_scan(self, network=None, fast_mode=False):
        """Comprehensive Windows host discovery"""
        start_time = time.time()
        
        if network is None:
            networks = self.get_local_networks()
            print(f"{Colors.CYAN}Auto-detected networks: {', '.join(networks)}{Colors.END}")
        else:
            networks = [network]
        
        all_windows_hosts = []
        
        for net in networks:
            print(f"\n{Colors.BOLD}Scanning network: {net}{Colors.END}")
            
            # Step 1: Ping sweep to find live hosts
            live_hosts = self.ping_sweep(net)
            
            if not live_hosts:
                print(f"{Colors.YELLOW}No live hosts found in {net}{Colors.END}")
                continue
            
            if fast_mode:
                # Fast mode: Only service detection
                windows_hosts = self.service_detection(live_hosts, max_workers=10)
            else:
                # Comprehensive mode: OS detection + service detection
                print(f"\n{Colors.CYAN}Running comprehensive scan...{Colors.END}")
                
                # Step 2: OS detection (threaded)
                os_detected = self.detect_os_threaded(live_hosts, max_workers=5)
                
                # Step 3: Service detection on all live hosts
                service_detected = self.service_detection(live_hosts, max_workers=8)
                
                # Combine results
                windows_hosts = []
                
                # Add OS-detected Windows hosts
                for host in os_detected:
                    windows_hosts.append({
                        'ip': host['ip'],
                        'detection_method': 'OS Detection',
                        'os': host['os'],
                        'accuracy': host['accuracy'],
                        'services': []
                    })
                
                # Add service-detected Windows hosts
                for host in service_detected:
                    # Check if already added by OS detection
                    existing = next((h for h in windows_hosts if h['ip'] == host['ip']), None)
                    if existing:
                        existing['services'] = host['services']
                        existing['detection_method'] = 'OS Detection + Service Detection'
                    else:
                        windows_hosts.append({
                            'ip': host['ip'],
                            'detection_method': 'Service Detection',
                            'os': 'Unknown (Windows services detected)',
                            'accuracy': 0,
                            'services': host['services']
                        })
            
            all_windows_hosts.extend(windows_hosts)
        
        elapsed_time = time.time() - start_time
        
        # Display results
        print(f"\n{Colors.BOLD}=== SCAN RESULTS ==={Colors.END}")
        print(f"{Colors.CYAN}Scan completed in {elapsed_time:.2f} seconds{Colors.END}")
        print(f"{Colors.GREEN}Found {len(all_windows_hosts)} potential Windows targets:{Colors.END}\n")
        
        for i, host in enumerate(all_windows_hosts, 1):
            print(f"{Colors.BOLD}{i}. {host['ip']}{Colors.END}")
            print(f"   Detection: {host['detection_method']}")
            if host.get('os'):
                print(f"   OS: {host['os']}")
            if host.get('accuracy'):
                print(f"   Accuracy: {host['accuracy']}%")
            if host.get('services'):
                print(f"   Windows Services:")
                for service in host['services']:
                    print(f"     - Port {service['port']}: {service['service']} ({service['product']})")
            print()
        
        return all_windows_hosts

    def quick_port_scan(self, target_ip, ports=None):
        """Quick port scan with service detection"""
        if ports is None:
            # Common Windows ports
            ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 1521, 1723, 3389, 5985, 5986]
        
        print(f"{Colors.CYAN}Scanning {target_ip} for open ports...{Colors.END}")
        
        try:
            port_list = ','.join(map(str, ports))
            self.nm.scan(target_ip, port_list, arguments='-sV -T4 --max-retries 2')
            
            if target_ip in self.nm.all_hosts():
                host_info = self.nm[target_ip]
                
                print(f"{Colors.GREEN}Scan results for {target_ip}:{Colors.END}")
                print(f"Host state: {host_info.state()}")
                
                for protocol in host_info.all_protocols():
                    ports_info = host_info[protocol].keys()
                    for port in sorted(ports_info):
                        port_info = host_info[protocol][port]
                        state = port_info['state']
                        service = port_info.get('name', 'unknown')
                        product = port_info.get('product', '')
                        version = port_info.get('version', '')
                        
                        color = Colors.GREEN if state == 'open' else Colors.YELLOW
                        print(f"{color}Port {port}/{protocol}: {state} - {service} {product} {version}{Colors.END}")
                
                return True
            else:
                print(f"{Colors.RED}Host {target_ip} appears to be down or unreachable{Colors.END}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}Port scan failed: {e}{Colors.END}")
            return False

    def list_live_ips(self, network=None, timeout=3):
        """List all live IP addresses on local networks or a specified CIDR."""
        if network is None:
            networks = self.get_local_networks()
            print(f"{Colors.CYAN}Auto-detected networks: {', '.join(networks)}{Colors.END}")
        else:
            networks = [network]

        all_live = []
        for net in networks:
            live = self.ping_sweep(net, timeout=timeout)
            all_live.extend(live)

        unique_live = sorted(set(all_live), key=lambda ip: tuple(int(x) for x in ip.split('.')))

        print(f"\n{Colors.BOLD}=== LIVE HOSTS ==={Colors.END}")
        print(f"{Colors.GREEN}Found {len(unique_live)} live IPs{Colors.END}")
        for ip in unique_live:
            print(ip)

        return unique_live
