import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN n'est pas défini dans le fichier .env")

# Configuration des téléchargements
DOWNLOAD_PATH = "downloads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (limite Telegram)
SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']

# Configuration des messages
MESSAGES = {
    'welcome': "🎬 Bienvenue au Bot de Téléchargement de Vidéos!\n\n"
               "Envoyez-moi un lien vers une vidéo et je la téléchargerai pour vous.\n"
               "Exemple: https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4",
    'processing': "⏳ Traitement en cours...",
    'downloading': "📥 Téléchargement en cours...",
    'uploading': "📤 Envoi en cours...",
    'success': "✅ Vidéo envoyée avec succès!",
    'error': "❌ Erreur lors du traitement de la vidéo",
    'invalid_url': "❌ Lien invalide ou non supporté",
    'file_too_large': "❌ Le fichier est trop volumineux (max 50MB)",
    'not_found': "❌ Vidéo non trouvée"
} 