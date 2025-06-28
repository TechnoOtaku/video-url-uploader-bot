<<<<<<< HEAD
# video-url-uploader-bot
=======
# 🎬 Bot Telegram de Téléchargement de Vidéos

Un bot Telegram intelligent qui peut télécharger des vidéos depuis des liens et les envoyer directement aux utilisateurs avec un **suivi de progression en temps réel**.

## ✨ Fonctionnalités

- 📥 Téléchargement de vidéos depuis de nombreux sites (YouTube, Vimeo, Sibnet, etc.)
- 📤 Envoi direct des vidéos aux utilisateurs
- 📊 **Suivi de progression en temps réel** avec :
  - Barre de progression visuelle
  - Vitesse de téléchargement en MB/s
  - Temps restant estimé
  - Pourcentage de progression
  - Taille téléchargée / taille totale
- 🎯 Interface utilisateur intuitive avec boutons inline
- 🛡️ Gestion des erreurs et nettoyage automatique des fichiers
- 📱 Support de multiples formats vidéo (MP4, AVI, MOV, MKV, WEBM)
- 🔄 Mise à jour automatique toutes les 2 secondes

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Un bot Telegram (créé via @BotFather)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <repository-url>
   cd "Video Url uploader Bot"
   ```

2. **Configuration automatique**
   ```bash
   python setup.py
   ```

3. **Créer un environnement virtuel**
   ```bash
   python -m venv .venv
   ```

4. **Activer l'environnement virtuel**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

5. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

6. **Configurer le bot**
   - Copiez le fichier `env_example.txt` vers `.env`
   - Remplacez `YOUR_BOT_TOKEN` par votre véritable token de bot Telegram

   ```bash
   copy env_example.txt .env
   ```

   Puis éditez le fichier `.env` et ajoutez votre token:
   ```
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

## 🎯 Utilisation

### Démarrage du bot

```bash
python main.py
```

### Utilisation avec les utilisateurs

1. **Démarrer le bot**: Envoyez `/start` au bot
2. **Télécharger une vidéo**: Envoyez simplement le lien de la vidéo
3. **Suivre la progression**: Le bot affiche en temps réel :
   - 📊 Pourcentage de progression
   - ⚡ Vitesse de téléchargement
   - ⏱️ Temps restant estimé
   - 📁 Taille téléchargée / taille totale
4. **Recevoir la vidéo**: La vidéo est envoyée automatiquement

### Exemple de lien
```
https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4
```

### Commandes disponibles

- `/start` - Démarrer le bot et afficher le menu principal
- `/help` - Afficher l'aide et les instructions

## 📁 Structure du projet

```
Video Url uploader Bot/
├── main.py              # Point d'entrée principal
├── config.py            # Configuration et variables d'environnement
├── telegram_bot.py      # Logique principale du bot Telegram
├── video_downloader.py  # Module de téléchargement de vidéos avec progression
├── requirements.txt     # Dépendances Python
├── env_example.txt      # Exemple de configuration
├── setup.py            # Script de configuration automatique
├── test_bot.py         # Tests du bot
├── demo_progress.py    # Démonstration des fonctionnalités de progression
├── README.md           # Ce fichier
├── QUICKSTART.md       # Guide de démarrage rapide
└── downloads/          # Dossier de téléchargement (créé automatiquement)
```

## ⚙️ Configuration

### Variables d'environnement

- `BOT_TOKEN`: Token de votre bot Telegram (obligatoire)

### Paramètres configurables

Dans `config.py`, vous pouvez modifier:

- `MAX_FILE_SIZE`: Taille maximale des fichiers (défaut: 50MB)
- `SUPPORTED_FORMATS`: Formats vidéo supportés
- `DOWNLOAD_PATH`: Dossier de téléchargement
- `MESSAGES`: Messages personnalisés du bot

## 🔧 Fonctionnalités techniques

### Suivi de progression en temps réel

Le bot affiche en temps réel (mise à jour toutes les 2 secondes) :

```
📥 Téléchargement en cours...

📊 Progression: 45.2%
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
██████████░░░░░░░░░░

📁 Téléchargé: 11.5 MB / 25.5 MB
⚡ Vitesse: 2.8 MB/s
⏱️ Temps restant: 5m 12s
```

### Fonctionnalités de progression

- **Barre de progression visuelle** : Affichage graphique de l'avancement
- **Vitesse en temps réel** : Calcul automatique de la vitesse de téléchargement
- **Estimation du temps** : Calcul intelligent du temps restant
- **Informations détaillées** : Taille téléchargée, taille totale, pourcentage
- **Mise à jour automatique** : Actualisation toutes les 2 secondes

### Gestion des erreurs

- Validation des URLs
- Vérification de la taille des fichiers
- Gestion des téléchargements simultanés
- Nettoyage automatique des fichiers temporaires
- Gestion des erreurs de réseau

### Sites supportés

Le bot utilise `yt-dlp` qui supporte de nombreux sites:
- YouTube
- Vimeo
- Dailymotion
- Sibnet
- Et bien d'autres...

## 🧪 Tests et démonstration

### Tests du bot
```bash
python test_bot.py
```

### Démonstration des fonctionnalités de progression
```bash
python demo_progress.py
```

## 🛠️ Développement

### Ajouter de nouveaux sites

Le bot utilise `yt-dlp` qui supporte automatiquement de nombreux sites. Si un site n'est pas supporté, vous pouvez:

1. Vérifier la compatibilité sur [yt-dlp](https://github.com/yt-dlp/yt-dlp)
2. Ajouter des extracteurs personnalisés si nécessaire

### Personnalisation

Vous pouvez personnaliser:
- Les messages du bot dans `config.py`
- Les formats de sortie dans `video_downloader.py`
- L'interface utilisateur dans `telegram_bot.py`
- La fréquence de mise à jour de progression (actuellement 2 secondes)

### Architecture de progression

Le système de progression utilise :
- **Hook de progression yt-dlp** : Capture les données de téléchargement
- **Stockage en mémoire** : Stockage temporaire des données de progression par utilisateur
- **Tâches asynchrones** : Mise à jour non-bloquante des messages
- **Formatage intelligent** : Affichage lisible des vitesses et temps

## 📝 Logs

Le bot génère des logs détaillés pour:
- Les téléchargements avec progression
- Les erreurs
- Les interactions utilisateur
- Les performances

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à:
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

Si vous rencontrez des problèmes:

1. Vérifiez que toutes les dépendances sont installées
2. Assurez-vous que votre token de bot est correct
3. Consultez les logs pour plus d'informations
4. Vérifiez que l'URL de la vidéo est accessible
5. Testez avec `python test_bot.py`

## 🎉 Exemple d'utilisation complète

```
Utilisateur: /start
Bot: 🎬 Bienvenue au Bot de Téléchargement de Vidéos!

Utilisateur: https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4
Bot: ⏳ Initialisation...

Bot: 📥 Téléchargement en cours...
📊 Progression: 25.0%
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
█████░░░░░░░░░░░░░░░
📁 Téléchargé: 6.4 MB / 25.5 MB
⚡ Vitesse: 2.1 MB/s
⏱️ Temps restant: 9m 15s

Bot: 📥 Téléchargement en cours...
📊 Progression: 75.0%
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
███████████████░░░░░
📁 Téléchargé: 19.1 MB / 25.5 MB
⚡ Vitesse: 3.2 MB/s
⏱️ Temps restant: 2m 5s

Bot: 📤 Envoi en cours...
Bot: ✅ Téléchargement et envoi terminés!
```

---

**Développé avec ❤️ pour simplifier le partage de vidéos sur Telegram avec suivi de progression en temps réel** 
>>>>>>> 580aebe (Initial commit: Telegram video uploader bot)
