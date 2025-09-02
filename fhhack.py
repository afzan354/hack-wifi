#!/usr/bin/env python3
"""
WiFi Password Generator - Python Version
By Afzan
"""

import os
import sys
import time
import subprocess
from typing import Optional

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    """Display the ASCII art banner"""
    clear_screen()
    print(f"{Colors.CYAN}")
    print("██╗    ██╗██╗███████╗██╗     ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ ")
    print("██║    ██║██║██╔════╝██║    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗")
    print("██║ █╗ ██║██║█████╗  ██║    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝")
    print("██║███╗██║██║██╔══╝  ██║    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗")
    print("╚███╔███╔╝██║██║     ██║    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║")
    print(" ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝")
    print(f"{Colors.NC}")
    print(f"{Colors.PURPLE}                                          By Afzan{Colors.NC}")
    print(f"{Colors.WHITE}{'═' * 115}{Colors.NC}")
    print()

def get_character_mapping() -> dict:
    """Create the character mapping dictionary"""
    pairs = [
        ('a', '5'), ('b', '4'), ('c', '3'), 
        ('d', '2'), ('e', '1'), ('f', '0'),
        ('6', '9'), ('7', '8')
    ]
    
    mapping = {}
    for pair in pairs:
        mapping[pair[0]] = pair[1]
        mapping[pair[1]] = pair[0]
    
    return mapping

def generate_password(ssid: str) -> Optional[str]:
    """Generate password from SSID using the mapping algorithm"""
    # Check if SSID starts with 'fh_'
    if not ssid.startswith('fh_'):
        return None
    
    # Split by underscore
    parts = ssid.split('_')
    if len(parts) < 2:
        return None
    
    middle = parts[1]
    result = "wlan"
    
    # Get character mapping
    char_map = get_character_mapping()
    
    # Map each character in the middle part
    for char in middle:
        char_lower = char.lower()
        if char_lower in char_map:
            result += char_map[char_lower]
        else:
            result += char
    
    # Add remaining parts (except '5G')
    for i in range(2, len(parts)):
        if parts[i] != '5G':
            result += '_' + parts[i]
    
    return result

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard if possible"""
    try:
        # For Termux
        if subprocess.run(['which', 'termux-clipboard-set'], 
                         capture_output=True, text=True).returncode == 0:
            subprocess.run(['termux-clipboard-set'], input=text, text=True)
            return True
        # For Linux with xclip
        elif subprocess.run(['which', 'xclip'], 
                           capture_output=True, text=True).returncode == 0:
            subprocess.run(['xclip', '-selection', 'clipboard'], 
                          input=text, text=True)
            return True
        # For macOS
        elif subprocess.run(['which', 'pbcopy'], 
                           capture_output=True, text=True).returncode == 0:
            subprocess.run(['pbcopy'], input=text, text=True)
            return True
    except:
        pass
    return False

def print_loading():
    """Show loading animation"""
    print(f"{Colors.YELLOW}⚡ Generating password", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(f"{Colors.NC}")
    time.sleep(0.5)

def main():
    """Main function"""
    while True:
        show_banner()
        
        print(f"{Colors.YELLOW}🔐 WiFi Password Generator{Colors.NC}")
        print(f"{Colors.WHITE}{'━' * 30}{Colors.NC}")
        print()
        
        # Input section
        print(f"{Colors.CYAN}📡 Masukkan SSID WiFi:{Colors.NC}")
        print(f"{Colors.WHITE}   Format: {Colors.YELLOW}fh_xxxxxx_5G{Colors.NC}")
        print(f"{Colors.WHITE}   Contoh: {Colors.GREEN}fh_b894f8_5G{Colors.NC}")
        print()
        
        try:
            ssid = input(f"{Colors.BLUE}SSID: {Colors.WHITE}").strip()
            print(f"{Colors.NC}")
            
            # Validate input
            if not ssid:
                print(f"{Colors.RED}❌ SSID tidak boleh kosong!{Colors.NC}")
                time.sleep(2)
                continue
            
            # Generate password
            print_loading()
            
            password = generate_password(ssid)
            
            if password:
                print(f"{Colors.GREEN}✅ Password berhasil di-generate!{Colors.NC}")
                print(f"{Colors.WHITE}{'━' * 42}{Colors.NC}")
                print(f"{Colors.CYAN}📋 SSID:     {Colors.WHITE}{ssid}{Colors.NC}")
                print(f"{Colors.CYAN}🔑 Password: {Colors.GREEN}{password}{Colors.NC}")
                print(f"{Colors.WHITE}{'━' * 42}{Colors.NC}")
                
                # Try to copy to clipboard
                if copy_to_clipboard(password):
                    print(f"{Colors.GREEN}📋 Password sudah disalin ke clipboard!{Colors.NC}")
                else:
                    print(f"{Colors.YELLOW}💡 Salin password secara manual jika diperlukan{Colors.NC}")
            else:
                print(f"{Colors.RED}❌ Error: SSID tidak valid. Pastikan format dimulai dengan 'fh_' dan memiliki kode yang benar.{Colors.NC}")
            
            print()
            print(f"{Colors.YELLOW}Pilihan:{Colors.NC}")
            print(f"{Colors.WHITE}1. {Colors.GREEN}Generate lagi{Colors.NC}")
            print(f"{Colors.WHITE}2. {Colors.RED}Keluar{Colors.NC}")
            print()
            
            choice = input(f"{Colors.BLUE}Pilih (1/2): {Colors.WHITE}").strip()
            print(f"{Colors.NC}")
            
            if choice == '2':
                print(f"{Colors.PURPLE}Terima kasih telah menggunakan WiFi Generator!{Colors.NC}")
                print(f"{Colors.CYAN}© 2025 By Afzan{Colors.NC}")
                sys.exit(0)
            elif choice not in ['1', '']:
                print(f"{Colors.RED}Pilihan tidak valid!{Colors.NC}")
                time.sleep(2)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.PURPLE}Terima kasih telah menggunakan WiFi Generator!{Colors.NC}")
            print(f"{Colors.CYAN}© 2025 By Afzan{Colors.NC}")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}❌ Terjadi kesalahan: {str(e)}{Colors.NC}")
            time.sleep(2)

if __name__ == "__main__":
    main()
