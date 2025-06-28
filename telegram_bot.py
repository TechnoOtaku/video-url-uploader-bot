import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import re

from config import BOT_TOKEN, MESSAGES, MAX_FILE_SIZE
from video_downloader import VideoDownloader

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class VideoUploaderBot:
    def __init__(self):
        self.downloader = VideoDownloader()
        self.active_downloads = {}  # Pour suivre les téléchargements actifs
        self.progress_tasks = {}  # Pour les tâches de mise à jour de progression
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        keyboard = [
            [InlineKeyboardButton("📥 Télécharger une vidéo", callback_data="download_info")],
            [InlineKeyboardButton("ℹ️ Aide", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            MESSAGES['welcome'],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        help_text = """
🎬 <b>Bot de Téléchargement de Vidéos</b>

<b>Comment utiliser:</b>
1. Envoyez-moi un lien vers une vidéo
2. Je téléchargerai la vidéo pour vous avec suivi en temps réel
3. Je vous l'enverrai directement

<b>Sites supportés:</b>
• YouTube
• Vimeo
• Dailymotion
• Sibnet
• Et bien d'autres...

<b>Fonctionnalités:</b>
• 📊 Suivi de progression en temps réel
• ⚡ Affichage de la vitesse de téléchargement
• ⏱️ Temps restant estimé
• 📁 Informations détaillées sur le fichier

<b>Limitations:</b>
• Taille maximale: 50MB
• Formats supportés: MP4, AVI, MOV, MKV, WEBM

<b>Commandes:</b>
/start - Démarrer le bot
/help - Afficher cette aide
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
    
    async def handle_url_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les messages contenant des URLs"""
        message = update.message.text
        user_id = update.effective_user.id
        
        # Extraire les URLs du message
        urls = self._extract_urls(message)
        
        if not urls:
            await update.message.reply_text(
                "❌ Aucune URL valide trouvée dans votre message.\n"
                "Envoyez-moi un lien vers une vidéo.",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Traiter chaque URL
        for url in urls:
            await self._process_video_url(update, context, url, user_id)
    
    def _extract_urls(self, text: str) -> list:
        """Extrait les URLs d'un texte"""
        url_pattern = re.compile(
            r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        )
        return url_pattern.findall(text)
    
    async def _update_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, status_message):
        """Met à jour le message de progression"""
        try:
            while user_id in self.active_downloads:
                # Obtenir les informations de progression
                progress_message = self.downloader.format_progress_message(user_id)
                
                # Mettre à jour le message
                await status_message.edit_text(
                    progress_message,
                    parse_mode=ParseMode.HTML
                )
                
                # Attendre 2 secondes avant la prochaine mise à jour
                await asyncio.sleep(2)
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de progression: {e}")
    
    async def _process_video_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE, url: str, user_id: int):
        """Traite une URL de vidéo avec suivi de progression"""
        try:
            # Message de statut initial
            status_message = await update.message.reply_text(
                f"⏳ <b>Initialisation...</b>\n\n"
                f"🔗 URL: <code>{url}</code>",
                parse_mode=ParseMode.HTML
            )
            
            # Vérifier si l'utilisateur a déjà un téléchargement en cours
            if user_id in self.active_downloads:
                await status_message.edit_text(
                    "⚠️ Vous avez déjà un téléchargement en cours.\n"
                    "Veuillez attendre qu'il se termine.",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Marquer le téléchargement comme actif
            self.active_downloads[user_id] = True
            
            # Démarrer la tâche de mise à jour de progression
            progress_task = asyncio.create_task(
                self._update_progress(update, context, user_id, status_message)
            )
            self.progress_tasks[user_id] = progress_task
            
            # Télécharger la vidéo avec suivi de progression
            downloaded_file = await self.downloader.download_video(url, user_id)
            
            # Arrêter la tâche de progression
            if user_id in self.progress_tasks:
                self.progress_tasks[user_id].cancel()
                del self.progress_tasks[user_id]
            
            if not downloaded_file:
                await status_message.edit_text(
                    f"❌ <b>Échec du téléchargement</b>\n\n"
                    f"🔗 URL: <code>{url}</code>\n"
                    f"💡 Vérifiez que le lien est valide et accessible.",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Obtenir les informations du fichier
            file_info = self.downloader.get_file_info(downloaded_file)
            
            # Message de préparation de l'envoi
            await status_message.edit_text(
                f"📤 <b>Envoi en cours...</b>\n\n"
                f"📁 Fichier: <code>{file_info.get('name', 'video')}</code>\n"
                f"📊 Taille: <code>{file_info.get('size_mb', 0):.2f} MB</code>\n"
                f"⏳ Préparation de l'envoi...",
                parse_mode=ParseMode.HTML
            )
            
            # Envoyer la vidéo
            try:
                with open(downloaded_file, 'rb') as video_file:
                    await context.bot.send_video(
                        chat_id=update.effective_chat.id,
                        video=video_file,
                        caption=f"🎬 <b>Vidéo téléchargée avec succès!</b>\n\n"
                                f"📁 Nom: <code>{file_info.get('name', 'video')}</code>\n"
                                f"📊 Taille: <code>{file_info.get('size_mb', 0):.2f} MB</code>\n"
                                f"🔗 Source: <code>{url}</code>\n"
                                f"✅ Téléchargement terminé",
                        parse_mode=ParseMode.HTML
                    )
                
                # Message de succès final
                await status_message.edit_text(
                    f"✅ <b>Téléchargement et envoi terminés!</b>\n\n"
                    f"📁 Fichier: <code>{file_info.get('name', 'video')}</code>\n"
                    f"📊 Taille: <code>{file_info.get('size_mb', 0):.2f} MB</code>\n"
                    f"🎉 Vidéo envoyée avec succès!",
                    parse_mode=ParseMode.HTML
                )
                
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de la vidéo: {e}")
                await status_message.edit_text(
                    f"❌ <b>Erreur lors de l'envoi</b>\n\n"
                    f"🔗 URL: <code>{url}</code>\n"
                    f"💡 Le fichier pourrait être trop volumineux.",
                    parse_mode=ParseMode.HTML
                )
            
            finally:
                # Nettoyer le fichier téléchargé
                await self.downloader.cleanup_file(downloaded_file)
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'URL {url}: {e}")
            await update.message.reply_text(
                f"❌ <b>Erreur lors du traitement</b>\n\n"
                f"🔗 URL: <code>{url}</code>\n"
                f"💡 Veuillez réessayer plus tard.",
                parse_mode=ParseMode.HTML
            )
        
        finally:
            # Retirer le téléchargement de la liste active
            self.active_downloads.pop(user_id, None)
            
            # Annuler la tâche de progression si elle existe encore
            if user_id in self.progress_tasks:
                self.progress_tasks[user_id].cancel()
                del self.progress_tasks[user_id]
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les callbacks des boutons inline"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "download_info":
            help_text = """
📥 <b>Comment télécharger une vidéo:</b>

1. <b>Copiez le lien</b> de la vidéo que vous voulez télécharger
2. <b>Collez-le ici</b> dans le chat
3. <b>Suivez la progression</b> en temps réel avec:
   • 📊 Pourcentage de progression
   • ⚡ Vitesse de téléchargement
   • ⏱️ Temps restant estimé
4. <b>Recevez la vidéo</b> directement

<b>Exemple de lien:</b>
<code>https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4</code>

<b>Fonctionnalités avancées:</b>
• Suivi de progression en temps réel
• Affichage de la vitesse de téléchargement
• Estimation du temps restant
• Barre de progression visuelle

<b>Limitations:</b>
• Taille maximale: 50MB
• Formats supportés: MP4, AVI, MOV, MKV, WEBM
            """
            await query.edit_message_text(help_text, parse_mode=ParseMode.HTML)
        
        elif query.data == "help":
            await self.help_command(update, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les erreurs du bot"""
        logger.error(f"Exception lors de la mise à jour {update}: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Une erreur s'est produite. Veuillez réessayer plus tard."
            )
    
    def run(self):
        """Lance le bot"""
        # Créer l'application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Ajouter les handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_url_message))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Ajouter le gestionnaire d'erreurs
        application.add_error_handler(self.error_handler)
        
        # Démarrer le bot
        logger.info("Bot démarré avec suivi de progression en temps réel...")
        application.run_polling(allowed_updates=Update.ALL_TYPES) 