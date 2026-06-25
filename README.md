# Dacia 2.0 - Systeme de Securisation de Cle USB

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.x-green)
![Licence](https://img.shields.io/badge/licence-MIT-orange)

**Dacia 2.0** transforme une cle USB en coffre-fort numerique pour fichiers audio.

## Fonctionnalites

- Authentification SHA-256
- Filtrage audio uniquement (.mp3, .wav, .flac, .m4a)
- Analyse des signatures binaires (Magic Numbers)
- Verrouillage lecture seule (chmod 444)
- Blocage documents, videos, executables

## Installation

### Linux (Ubuntu, Debian, Mint)

sudo apt update
sudo apt install git python3 -y
git clone https://github.com/PenielLoi/Dacia-2.0.git
cd Dacia-2.0
chmod +x install.sh
bash install.sh
sudo python3 dacia.py

### macOS

brew install python3 git
git clone https://github.com/PenielLoi/Dacia-2.0.git
cd Dacia-2.0
chmod +x install.sh
bash install.sh
sudo python3 dacia.py

### Windows

git clone https://github.com/PenielLoi/Dacia-2.0.git
cd Dacia-2.0
python dacia.py

## Utilisation

sudo python3 dacia.py

## Support

losilopeniels2@gmail.com

## Licence

MIT License
