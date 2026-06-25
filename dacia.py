#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dacia 2.0 - Système de Sécurisation de Clé USB
Copyright (c) 2025 Projet Dacia 2.0
Support : losilopeniels2@gmail.com
Licence : MIT
"""

import os
import hashlib
import sys

# =====================================================================
# CONFIGURATION
# =====================================================================
USB_MOUNT_NAME = "UNTITLED"
USB_PATH = f"/mnt/chromeos/removable/{USB_MOUNT_NAME}"
VAULT_PATH = os.path.join(USB_PATH, ".dacia_vault")
PASSWORD_FILE = os.path.join(VAULT_PATH, ".sys_config.dat")
SUPPORT_EMAIL = "losilopeniels2@gmail.com"
VERSION = "2.0.0"

ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.m4a']
BLOCKED_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.txt', '.pdf', '.doc', '.docx', '.exe', '.sh', '.bat', '.msi']

AUDIO_SIGNATURES = {
    b'ID3': 'mp3',
    b'\xff\xfb': 'mp3',
    b'\xff\xf3': 'mp3',
    b'\xff\xf2': 'mp3',
    b'RIFF': 'wav',
    b'fLaC': 'flac',
    b'ftyp': 'm4a',
    b'OggS': 'ogg',
}

def banniere():
    print("""
╔══════════════════════════════════════════╗
║          🔒 DACIA 2.0 🔒               ║
║   Système de Protection de Clé USB     ║
║          Version {}                  ║
║  Support : {}  ║
╚══════════════════════════════════════════╝
    """.format(VERSION, SUPPORT_EMAIL))

def verifier_cle():
    if not os.path.exists(USB_PATH):
        print(f"[-] Erreur : La clé USB '{USB_MOUNT_NAME}' n'est pas détectée.")
        print("[-] Actions à effectuer :")
        print("    1. Branchez votre clé USB")
        print("    2. Ouvrez l'application Fichiers de Chrome OS")
        print(f"    3. Clic droit sur '{USB_MOUNT_NAME}' -> Partager avec Linux")
        return False
    return True

def initialiser_dacia():
    if not verifier_cle():
        return False
    if not os.path.exists(VAULT_PATH):
        try:
            os.makedirs(VAULT_PATH, exist_ok=True)
            os.chmod(VAULT_PATH, 0o700)
            print("[+] Coffre-fort Dacia 2.0 créé avec succès sur la clé.")
        except Exception as e:
            print(f"[-] Erreur lors de la création du coffre-fort : {e}")
            return False
    return True

def verifier_mot_de_passe():
    if not os.path.exists(PASSWORD_FILE):
        print("\n" + "="*50)
        print("     CONFIGURATION INITIALE DE DACIA 2.0")
        print(f"     Assistance : {SUPPORT_EMAIL}")
        print("="*50 + "\n")
        pwd = input("🔑 Définissez votre code secret maître : ")
        if len(pwd) < 4:
            print("[-] Sécurité insuffisante. 4 caractères minimum requis.")
            return False
        pwd_confirm = input("🔑 Confirmez votre code secret : ")
        if pwd != pwd_confirm:
            print("[-] Les codes ne correspondent pas.")
            return False
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        try:
            with open(PASSWORD_FILE, 'w') as f:
                f.write(hashed)
            os.chmod(PASSWORD_FILE, 0o400)
            print("[+] Code secret configuré avec succès !")
            print("[!] IMPORTANT : Retenez ce code, il est irrécupérable.")
            return True
        except Exception as e:
            print(f"[-] Erreur lors de la sauvegarde : {e}")
            return False
    else:
        tentatives = 3
        while tentatives > 0:
            pwd = input(f"\n🔒 Mot de passe Dacia 2.0 ({tentatives} tentative(s)) : ")
            hashed = hashlib.sha256(pwd.encode()).hexdigest()
            try:
                with open(PASSWORD_FILE, 'r') as f:
                    stored = f.read().strip()
            except Exception:
                print("[-] Fichier de configuration corrompu.")
                return False
            if hashed == stored:
                print("[+] Clé USB déverrouillée. Bienvenue !")
                return True
            else:
                tentatives -= 1
                print(f"[-] Code incorrect. {tentatives} tentative(s) restante(s).")
        print("[-] ACCÈS BLOQUÉ. Trop de tentatives échouées.")
        print(f"[!] Contactez le support : {SUPPORT_EMAIL}")
        return False

def verifier_magic_number(chemin_fichier):
    try:
        with open(chemin_fichier, 'rb') as f:
            debut_fichier = f.read(4)
        for sig, format_name in AUDIO_SIGNATURES.items():
            if debut_fichier.startswith(sig):
                return True, format_name
        return False, None
    except Exception:
        return False, None

def analyser_et_stocker_fichier(fichier_source):
    if not os.path.exists(fichier_source):
        print("[-] Fichier source introuvable.")
        return False
    nom_fichier = os.path.basename(fichier_source)
    ext = os.path.splitext(nom_fichier)[1].lower()
    taille = os.path.getsize(fichier_source)
    print(f"\n{'='*50}")
    print(f"📁 Analyse de : {nom_fichier}")
    print(f"📏 Taille : {taille} octets")
    print(f"{'='*50}")
    if ext in BLOCKED_EXTENSIONS:
        print(f"[-] BLOCAGE : Format '{ext}' interdit.")
        return False
    if ext not in ALLOWED_EXTENSIONS:
        print(f"[-] BLOCAGE : Format '{ext}' non supporté.")
        return False
    est_audio, format_detecte = verifier_magic_number(fichier_source)
    if not est_audio:
        print("[-] ALERTE SÉCURITÉ : Signature binaire non conforme.")
        return False
    print(f"[+] Format audio détecté : {format_detecte.upper()}")
    if taille > 500 * 1024 * 1024:
        print("[-] Fichier trop volumineux (max 500 Mo).")
        return False
    destination = os.path.join(VAULT_PATH, nom_fichier)
    try:
        with open(fichier_source, 'rb') as src, open(destination, 'wb') as dst:
            dst.write(src.read())
        os.chmod(destination, 0o444)
        print(f"[+] ✅ Fichier sécurisé avec succès !")
        print(f"[!] Statut : LECTURE SEULE")
        return True
    except Exception as e:
        print(f"[-] Erreur : {e}")
        return False

def afficher_fichiers():
    print(f"\n📂 FICHIERS SÉCURISÉS SUR LA CLÉ")
    try:
        fichiers = [f for f in os.listdir(VAULT_PATH) if not f.startswith('.')]
        if not fichiers:
            print("  (Coffre-fort vide)")
        else:
            for i, f in enumerate(fichiers, 1):
                chemin = os.path.join(VAULT_PATH, f)
                taille = os.path.getsize(chemin)
                print(f"  {i}. {f} ({taille} octets) [🔒]")
            print(f"\n  Total : {len(fichiers)} fichier(s)")
    except Exception as e:
        print(f"[-] Erreur : {e}")

def supprimer_fichier():
    print(f"\n🗑️  SUPPRESSION DE FICHIER")
    try:
        fichiers = [f for f in os.listdir(VAULT_PATH) if not f.startswith('.')]
        if not fichiers:
            print("  Aucun fichier à supprimer.")
            return
        for i, f in enumerate(fichiers, 1):
            print(f"  {i}. {f}")
        choix = input("\nNuméro (0 pour annuler) : ")
        if choix == '0':
            return
        index = int(choix) - 1
        if 0 <= index < len(fichiers):
            nom = fichiers[index]
            conf = input(f"⚠️  Confirmer suppression de '{nom}' ? (OUI/non) : ")
            if conf.upper() == "OUI":
                os.remove(os.path.join(VAULT_PATH, nom))
                print(f"[+] '{nom}' supprimé.")
            else:
                print("[i] Annulé.")
    except Exception as e:
        print(f"[-] Erreur : {e}")

def menu_principal():
    while True:
        print(f"\n{'='*50}")
        print("        MENU DE SÉCURITÉ DACIA 2.0")
        print(f"{'='*50}")
        print("  1. ➕ Ajouter de la musique sécurisée")
        print("  2. 📂 Afficher les fichiers protégés")
        print("  3. 🗑️  Supprimer un fichier")
        print("  4. ℹ️  Informations système")
        print("  5. 🔒 Verrouiller et quitter")
        print(f"{'='*50}")
        choix = input("  Votre choix : ").strip()
        if choix == '1':
            fichier = input("\n📁 Chemin du fichier : ").strip()
            analyser_et_stocker_fichier(fichier)
        elif choix == '2':
            afficher_fichiers()
        elif choix == '3':
            supprimer_fichier()
        elif choix == '4':
            print(f"\n[ℹ️] Dacia 2.0 v{VERSION}")
            print(f"[ℹ️] Clé : {USB_PATH}")
            print(f"[ℹ️] Coffre : {VAULT_PATH}")
            print(f"[ℹ️] Support : {SUPPORT_EMAIL}")
        elif choix == '5':
            print("\n[*] Dacia 2.0 verrouillé. Données protégées.")
            break
        else:
            print("[-] Option invalide.")

if __name__ == "__main__":
    banniere()
    if os.geteuid() != 0:
        print("[-] Dacia 2.0 nécessite les privilèges ROOT.")
        print("[-] Relancez avec : sudo python3 dacia.py")
        sys.exit(1)
    if initialiser_dacia():
        if verifier_mot_de_passe():
            try:
                menu_principal()
            except KeyboardInterrupt:
                print("\n\n[*] Verrouillage d'urgence. Données protégées.")
