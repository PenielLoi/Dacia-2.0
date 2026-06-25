#!/bin/bash
clear
echo "============================================="
echo "   🔒 INSTALLATION DE DACIA 2.0 🔒"
echo "============================================="
echo ""

ROUGE='\033[0;31m'
VERT='\033[0;32m'
JAUNE='\033[1;33m'
BLEU='\033[0;34m'
NC='\033[0m'

echo -e "${BLEU}[*] Vérification de Python 3...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${VERT}[+] $PYTHON_VERSION détecté${NC}"
else
    echo -e "${ROUGE}[-] Python 3 non installé.${NC}"
    sudo apt-get update -y && sudo apt-get install python3 -y
fi

INSTALL_DIR="$HOME/Dacia-2.0"
mkdir -p "$INSTALL_DIR"

if [ -f "dacia.py" ]; then
    cp dacia.py "$INSTALL_DIR/"
    echo -e "${VERT}[+] dacia.py copié${NC}"
fi

chmod +x "$INSTALL_DIR/dacia.py"
echo -e "${VERT}[+] Droits appliqués${NC}"

ALIAS_LINE="alias dacia='sudo python3 $INSTALL_DIR/dacia.py'"
if grep -q "alias dacia=" "$HOME/.bashrc" 2>/dev/null; then
    sed -i "s|alias dacia=.*|$ALIAS_LINE|" "$HOME/.bashrc"
else
    echo "$ALIAS_LINE" >> "$HOME/.bashrc"
fi
echo -e "${VERT}[+] Alias 'dacia' créé${NC}"

echo ""
echo "============================================="
echo -e "${VERT}   ✅ INSTALLATION TERMINÉE !${NC}"
echo "============================================="
echo ""
echo "Utilisation : dacia"
echo "Support : losilopeniels2@gmail.com"
