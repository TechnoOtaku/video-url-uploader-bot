import os
import asyncio
import yt_dlp
import aiohttp
import logging
import time
from typing import Optional, Callable, Dict, Any
from config import DOWNLOAD_PATH, MAX_FILE_SIZE, SUPPORTED_FORMATS

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        self.download_path = DOWNLOAD_PATH
        os.makedirs(self.download_path, exist_ok=True)
        self.download_progress = {}  # Pour stocker les informations de progression
    
    def _progress_hook(self, d):
        """Hook pour suivre la progression du téléchargement"""
        if d['status'] == 'downloading':
            try:
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                
                if total > 0:
                    percentage = (downloaded / total) * 100
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    
                    # Calculer la vitesse en MB/s
                    speed_mb = speed / 1024 / 1024 if speed else 0
                    
                    # Formater le temps restant
                    eta_str = self._format_time(eta) if eta else "Calcul..."
                    
                    # Stocker les informations de progression
                    progress_info = {
                        'percentage': percentage,
                        'downloaded_mb': downloaded / 1024 / 1024,
                        'total_mb': total / 1024 / 1024,
                        'speed_mb': speed_mb,
                        'eta': eta_str,
                        'eta_seconds': eta,
                        'downloaded_bytes': downloaded,
                        'total_bytes': total
                    }
                    
                    # Stocker pour l'utilisateur actuel (si disponible)
                    if hasattr(self, 'current_user_id'):
                        self.download_progress[self.current_user_id] = progress_info
                    
                    logger.info(f"Progression: {percentage:.1f}% - Vitesse: {speed_mb:.2f} MB/s - Temps restant: {eta_str}")
                    
            except Exception as e:
                logger.error(f"Erreur dans le suivi de progression: {e}")
    
    def _format_time(self, seconds):
        """Formate le temps en secondes en format lisible"""
        if seconds is None or seconds < 0:
            return "Calcul..."
        
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def _format_size(self, bytes_size):
        """Formate la taille en bytes en format lisible"""
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.1f} KB"
        else:
            return f"{bytes_size / 1024 / 1024:.1f} MB"
    
    async def download_video(self, url: str, user_id: int = None, progress_callback: Optional[Callable] = None) -> Optional[str]:
        """
        Télécharge une vidéo depuis une URL avec suivi de progression
        
        Args:
            url: L'URL de la vidéo à télécharger
            user_id: ID de l'utilisateur pour le suivi de progression
            progress_callback: Fonction de callback pour le suivi de progression
            
        Returns:
            Le chemin du fichier téléchargé ou None si échec
        """
        try:
            # Stocker l'ID utilisateur pour le suivi
            if user_id:
                self.current_user_id = user_id
                self.download_progress[user_id] = {}
            
            # Configuration de yt-dlp avec suivi de progression amélioré
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'format': 'best[filesize<50M]/best',
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Vérifier si l'URL est valide
            if not self._is_valid_url(url):
                logger.error(f"URL invalide: {url}")
                return None
            
            # Télécharger la vidéo
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Début du téléchargement: {url}")
                
                # Obtenir les informations de la vidéo
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                duration = info.get('duration', 0)
                filesize = info.get('filesize', 0)
                
                logger.info(f"Titre: {title}")
                logger.info(f"Durée: {duration} secondes")
                logger.info(f"Taille estimée: {filesize / 1024 / 1024:.2f} MB")
                
                # Vérifier la taille du fichier
                if filesize > MAX_FILE_SIZE:
                    logger.error(f"Fichier trop volumineux: {filesize / 1024 / 1024:.2f} MB")
                    return None
                
                # Démarrer le téléchargement
                ydl.download([url])
                
                # Trouver le fichier téléchargé
                downloaded_file = self._find_downloaded_file(title)
                
                if downloaded_file and os.path.exists(downloaded_file):
                    file_size = os.path.getsize(downloaded_file)
                    logger.info(f"Téléchargement terminé: {downloaded_file} ({file_size / 1024 / 1024:.2f} MB)")
                    
                    # Nettoyer les données de progression
                    if user_id and user_id in self.download_progress:
                        del self.download_progress[user_id]
                    
                    return downloaded_file
                else:
                    logger.error("Fichier téléchargé non trouvé")
                    return None
                    
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement: {e}")
            return None
    
    def get_progress(self, user_id: int) -> Dict[str, Any]:
        """Obtient les informations de progression pour un utilisateur"""
        return self.download_progress.get(user_id, {})
    
    def format_progress_message(self, user_id: int) -> str:
        """Formate un message de progression pour l'affichage"""
        progress = self.get_progress(user_id)
        
        if not progress:
            return "⏳ Initialisation du téléchargement..."
        
        percentage = progress.get('percentage', 0)
        downloaded_mb = progress.get('downloaded_mb', 0)
        total_mb = progress.get('total_mb', 0)
        speed_mb = progress.get('speed_mb', 0)
        eta = progress.get('eta', 'Calcul...')
        
        # Créer une barre de progression
        bar_length = 20
        filled_length = int(bar_length * percentage / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        message = f"📥 <b>Téléchargement en cours...</b>\n\n"
        message += f"📊 <b>Progression:</b> {percentage:.1f}%\n"
        message += f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        message += f"<code>{bar}</code>\n\n"
        message += f"📁 <b>Téléchargé:</b> {downloaded_mb:.1f} MB / {total_mb:.1f} MB\n"
        message += f"⚡ <b>Vitesse:</b> {speed_mb:.2f} MB/s\n"
        message += f"⏱️ <b>Temps restant:</b> {eta}\n"
        
        return message
    
    def _is_valid_url(self, url: str) -> bool:
        """Vérifie si l'URL est valide"""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// ou https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domaine
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # port optionnel
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def _find_downloaded_file(self, title: str) -> Optional[str]:
        """Trouve le fichier téléchargé dans le dossier de téléchargement"""
        try:
            for filename in os.listdir(self.download_path):
                file_path = os.path.join(self.download_path, filename)
                if os.path.isfile(file_path):
                    # Vérifier si c'est un fichier vidéo supporté
                    if any(filename.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                        return file_path
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la recherche du fichier: {e}")
            return None
    
    async def cleanup_file(self, file_path: str):
        """Supprime un fichier téléchargé"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Fichier supprimé: {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du fichier: {e}")
    
    def get_file_info(self, file_path: str) -> dict:
        """Obtient les informations d'un fichier vidéo"""
        try:
            if not os.path.exists(file_path):
                return {}
            
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            return {
                'name': file_name,
                'size': file_size,
                'size_mb': file_size / 1024 / 1024,
                'path': file_path
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'obtention des informations du fichier: {e}")
            return {} 