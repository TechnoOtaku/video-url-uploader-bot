# 🚀 Guide de Démarrage Rapide

## Installation Express (5 minutes)

### 1. Configuration automatique
```bash
python setup.py
```

### 2. Créer votre bot Telegram
1. Ouvrez Telegram et cherchez **@BotFather**
2. Envoyez `/newbot`
3. Choisissez un nom pour votre bot
4. Choisissez un nom d'utilisateur (doit finir par 'bot')
5. Copiez le token fourni

### 3. Configurer le token
Éditez le fichier `.env` et remplacez `YOUR_BOT_TOKEN` par votre token :
```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4. Lancer le bot
```bash
python main.py
```

## 🎯 Utilisation

### Commandes de base
- `/start` - Démarrer le bot
- `/help` - Afficher l'aide

### Télécharger une vidéo
Envoyez simplement le lien de la vidéo au bot :
```
https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4
```

### Suivi de progression en temps réel
Le bot affiche automatiquement :
- 📊 **Pourcentage de progression** (ex: 45.2%)
- ⚡ **Vitesse de téléchargement** (ex: 2.8 MB/s)
- ⏱️ **Temps restant estimé** (ex: 5m 12s)
- 📁 **Taille téléchargée** (ex: 11.5 MB / 25.5 MB)
- ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ **Barre de progression visuelle**

## 🔧 Dépannage

### Erreur "BOT_TOKEN n'est pas défini"
- Vérifiez que le fichier `.env` existe
- Vérifiez que le token est correctement écrit

### Erreur de téléchargement
- Vérifiez que l'URL est accessible
- Vérifiez que la vidéo fait moins de 50MB

### Le bot ne répond pas
- Vérifiez que le bot est en cours d'exécution
- Vérifiez les logs dans la console

### Progression qui ne s'affiche pas
- Vérifiez votre connexion internet
- Certains sites peuvent ne pas fournir toutes les informations de progression

## 📱 Exemple d'utilisation complète

```
Vous: /start
Bot: 🎬 Bienvenue au Bot de Téléchargement de Vidéos!

Vous: https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4
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

## 🧪 Tests et démonstration

### Tester le bot
```bash
python test_bot.py
```

### Voir la démonstration de progression
```bash
python demo_progress.py
```

## 🆘 Besoin d'aide ?

- 📖 Documentation complète : `README.md`
- 🧪 Tests : `python test_bot.py`
- 🎬 Démonstration : `python demo_progress.py`
- 🔧 Configuration : `config.py`

## ✨ Nouvelles fonctionnalités

### Suivi de progression en temps réel
- **Mise à jour automatique** toutes les 2 secondes
- **Barre de progression visuelle** avec caractères Unicode
- **Calcul intelligent** de la vitesse et du temps restant
- **Informations détaillées** sur le téléchargement

### Interface améliorée
- Messages plus informatifs et visuellement attrayants
- Gestion des téléchargements simultanés
- Nettoyage automatique des fichiers temporaires

---

**🎉 Votre bot est prêt avec suivi de progression en temps réel !** 