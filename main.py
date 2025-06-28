#!/usr/bin/env python3
"""
Bot Telegram pour le téléchargement et l'envoi de vidéos
"""

import asyncio
import logging
import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import VideoUploaderBot
from config import BOT_TOKEN

def main():
    """Fonction principale"""
    # Configuration du logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Vérifier que le token est défini
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN n'est pas défini dans le fichier .env")
            print("❌ Erreur: BOT_TOKEN n'est pas défini dans le fichier .env")
            print("📝 Veuillez créer un fichier .env avec votre token de bot Telegram")
            return
        
        logger.info("🚀 Démarrage du Bot de Téléchargement de Vidéos...")
        print("🎬 Bot de Téléchargement de Vidéos")
        print("=" * 40)
        print("✅ Configuration chargée")
        print("✅ Modules importés")
        print("🚀 Démarrage du bot...")
        
        # Créer et lancer le bot
        bot = VideoUploaderBot()
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Arrêt du bot (Ctrl+C)")
        print("\n👋 Bot arrêté par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 