#!/usr/bin/env python3
"""
Script de configuration automatique pour le Bot Telegram de Téléchargement de Vidéos
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Affiche la bannière du script"""
    print("🎬 Bot Telegram de Téléchargement de Vidéos")
    print("=" * 50)
    print("Script de configuration automatique")
    print()

def check_python_version():
    """Vérifie la version de Python"""
    print("🔍 Vérification de la version Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou supérieur est requis")
        print(f"   Version actuelle: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} détecté")
    return True

def create_virtual_environment():
    """Crée un environnement virtuel"""
    print("\n🐍 Création de l'environnement virtuel...")
    
    if os.path.exists(".venv"):
        print("✅ Environnement virtuel déjà existant")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Environnement virtuel créé")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de la création de l'environnement virtuel")
        return False

def get_pip_command():
    """Retourne la commande pip appropriée"""
    if os.name == 'nt':  # Windows
        return os.path.join(".venv", "Scripts", "pip.exe")
    else:  # Linux/Mac
        return os.path.join(".venv", "bin", "pip")

def install_dependencies():
    """Installe les dépendances"""
    print("\n📦 Installation des dépendances...")
    
    pip_cmd = get_pip_command()
    
    if not os.path.exists(pip_cmd):
        print("❌ pip non trouvé dans l'environnement virtuel")
        return False
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dépendances installées")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation des dépendances")
        return False

def create_env_file():
    """Crée le fichier .env"""
    print("\n⚙️ Configuration du fichier .env...")
    
    if os.path.exists(".env"):
        print("✅ Fichier .env déjà existant")
        return True
    
    try:
        # Copier le fichier d'exemple
        if os.path.exists("env_example.txt"):
            shutil.copy("env_example.txt", ".env")
            print("✅ Fichier .env créé à partir de env_example.txt")
        else:
            # Créer un fichier .env basique
            with open(".env", "w") as f:
                f.write("# Configuration du Bot Telegram\n")
                f.write("BOT_TOKEN=YOUR_BOT_TOKEN\n")
            print("✅ Fichier .env créé")
        
        print("\n📝 IMPORTANT: Vous devez maintenant éditer le fichier .env")
        print("   et remplacer YOUR_BOT_TOKEN par votre véritable token de bot")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier .env: {e}")
        return False

def create_downloads_directory():
    """Crée le dossier de téléchargement"""
    print("\n📁 Création du dossier de téléchargement...")
    
    try:
        os.makedirs("downloads", exist_ok=True)
        print("✅ Dossier downloads créé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du dossier downloads: {e}")
        return False

def show_next_steps():
    """Affiche les prochaines étapes"""
    print("\n" + "=" * 50)
    print("🎉 Configuration terminée !")
    print("=" * 50)
    print("\n📋 Prochaines étapes:")
    print("1. 📱 Créez un bot Telegram via @BotFather")
    print("2. 🔑 Obtenez votre token de bot")
    print("3. ✏️ Éditez le fichier .env et remplacez YOUR_BOT_TOKEN")
    print("4. 🚀 Lancez le bot avec: python main.py")
    print("\n📖 Pour plus d'informations, consultez le README.md")
    print("\n🔗 Liens utiles:")
    print("   • @BotFather: https://t.me/BotFather")
    print("   • Documentation: README.md")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifications et installations
    steps = [
        ("Vérification Python", check_python_version),
        ("Création environnement virtuel", create_virtual_environment),
        ("Installation dépendances", install_dependencies),
        ("Configuration .env", create_env_file),
        ("Création dossier downloads", create_downloads_directory),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Échec à l'étape: {step_name}")
            print("💡 Vérifiez les erreurs ci-dessus et réessayez")
            return False
    
    show_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Configuration annulée par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1) 