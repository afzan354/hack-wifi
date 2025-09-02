#!/bin/bash

# WiFi Password Generator - Bash Version
# By Afzan

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ASCII Art
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "██╗    ██╗██╗███████╗██╗     ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ "
    echo "██║    ██║██║██╔════╝██║    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗"
    echo "██║ █╗ ██║██║█████╗  ██║    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝"
    echo "██║███╗██║██║██╔══╝  ██║    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗"
    echo "╚███╔███╔╝██║██║     ██║    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║"
    echo " ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
    echo -e "${NC}"
    echo -e "${PURPLE}                                          By Afzan${NC}"
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════${NC}"
    echo
}

# Character mapping function
map_character() {
    local char="$1"
    case "$char" in
        "a") echo "5" ;;
        "b") echo "4" ;;
        "c") echo "3" ;;
        "d") echo "2" ;;
        "e") echo "1" ;;
        "f") echo "0" ;;
        "5") echo "a" ;;
        "4") echo "b" ;;
        "3") echo "c" ;;
        "2") echo "d" ;;
        "1") echo "e" ;;
        "0") echo "f" ;;
        "6") echo "9" ;;
        "7") echo "8" ;;
        "9") echo "6" ;;
        "8") echo "7" ;;
        *) echo "$char" ;;
    esac
}

# Generate password function
generate_password() {
    local ssid="$1"
    
    # Check if SSID starts with 'fh_'
    if [[ ! "$ssid" =~ ^fh_.+ ]]; then
        echo -e "${RED}❌ Error: SSID harus dimulai dengan 'fh_'${NC}"
        return 1
    fi
    
    # Split SSID by underscore
    IFS='_' read -ra PARTS <<< "$ssid"
    
    if [ ${#PARTS[@]} -lt 2 ]; then
        echo -e "${RED}❌ Error: Format SSID tidak valid${NC}"
        return 1
    fi
    
    local middle="${PARTS[1]}"
    local result="wlan"
    
    # Convert each character in middle part
    for (( i=0; i<${#middle}; i++ )); do
        char="${middle:$i:1}"
        char_lower=$(echo "$char" | tr '[:upper:]' '[:lower:]')
        mapped_char=$(map_character "$char_lower")
        result="$result$mapped_char"
    done
    
    # Add remaining parts (except _5G)
    for (( i=2; i<${#PARTS[@]}; i++ )); do
        if [[ "${PARTS[$i]}" != "5G" ]]; then
            result="${result}_${PARTS[$i]}"
        fi
    done
    
    echo "$result"
}

# Main function
main() {
    show_banner
    
    while true; do
        echo -e "${YELLOW}🔐 WiFi Password Generator${NC}"
        echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo
        
        # Input SSID
        echo -e "${CYAN}📡 Masukkan SSID WiFi:${NC}"
        echo -e "${WHITE}   Format: ${YELLOW}fh_xxxxxx_5G${NC}"
        echo -e "${WHITE}   Contoh: ${GREEN}fh_b894f8_5G${NC}"
        echo
        echo -ne "${BLUE}SSID: ${WHITE}"
        read -r ssid
        
        echo
        
        # Validate input
        if [[ -z "$ssid" ]]; then
            echo -e "${RED}❌ SSID tidak boleh kosong!${NC}"
            echo
            continue
        fi
        
        # Generate password
        echo -e "${YELLOW}⚡ Generating password...${NC}"
        sleep 1
        
        password=$(generate_password "$ssid")
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Password berhasil di-generate!${NC}"
            echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${CYAN}📋 SSID:     ${WHITE}$ssid${NC}"
            echo -e "${CYAN}🔑 Password: ${GREEN}$password${NC}"
            echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            
            # Copy to clipboard (if available)
            if command -v termux-clipboard-set >/dev/null 2>&1; then
                echo "$password" | termux-clipboard-set
                echo -e "${GREEN}📋 Password sudah disalin ke clipboard!${NC}"
            elif command -v xclip >/dev/null 2>&1; then
                echo "$password" | xclip -selection clipboard
                echo -e "${GREEN}📋 Password sudah disalin ke clipboard!${NC}"
            fi
        fi
        
        echo
        echo -e "${YELLOW}Pilihan:${NC}"
        echo -e "${WHITE}1. ${GREEN}Generate lagi${NC}"
        echo -e "${WHITE}2. ${RED}Keluar${NC}"
        echo
        echo -ne "${BLUE}Pilih (1/2): ${WHITE}"
        read -r choice
        
        case "$choice" in
            1|"")
                echo
                continue
                ;;
            2)
                echo
                echo -e "${PURPLE}Terima kasih telah menggunakan WiFi Generator!${NC}"
                echo -e "${CYAN}© 2025 By Afzan${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Pilihan tidak valid!${NC}"
                sleep 2
                ;;
        esac
        
        echo
    done
}

# Run the main function
main
