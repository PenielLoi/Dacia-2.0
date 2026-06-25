# 🔒 Dacia 2.0 - Sécurisation de Clé USB

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.x-green)
![Licence](https://img.shields.io/badge/licence-MIT-orange)

**Dacia 2.0** transforme votre clé USB en coffre-fort sécurisé pour fichiers audio.

---

## 🛡️ Fonctionnalités

| Fonction | Description |
|----------|-------------|
| 🔐 Authentification | Mot de passe haché en SHA-256 |
| 🎵 Filtrage audio | Seuls .mp3 .wav .flac .m4a acceptés |
| 🧬 Anti-fraude | Analyse des signatures binaires réelles |
| 🔒 Verrouillage | Fichiers en lecture seule (chmod 444) |
| 🚫 Anti-malware | Bloque documents, vidéos, exécutables |

---

## 📥 Installation

### 🐧 Linux

```bash
sudo apt update && sudo apt install git python3 -y
git clone https://github.com/PenielLoi/Dacia-2.0.git
cd Dacia-2.0
bash install.sh
sudo python3 dacia.py
fin
