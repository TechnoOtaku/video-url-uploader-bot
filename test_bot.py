#!/usr/bin/env python3
"""
Script de test pour le Bot Telegram de Téléchargement de Vidéos
"""

import sys
import os
import asyncio
import logging

# Ajouter le répertoire courant au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Teste l'importation des modules"""
    print("🔍 Test des importations...")
    
    try:
        import config
        print("✅ config.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import config.py: {e}")
        return False
    
    try:
        from video_downloader import VideoDownloader
        print("✅ video_downloader.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import video_downloader.py: {e}")
        return False
    
    try:
        from telegram_bot import VideoUploaderBot
        print("✅ telegram_bot.py importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import telegram_bot.py: {e}")
        return False
    
    return True

def test_config():
    """Teste la configuration"""
    print("\n⚙️ Test de la configuration...")
    
    try:
        import config
        
        # Vérifier que les variables sont définies
        assert hasattr(config, 'DOWNLOAD_PATH'), "DOWNLOAD_PATH non défini"
        assert hasattr(config, 'MAX_FILE_SIZE'), "MAX_FILE_SIZE non défini"
        assert hasattr(config, 'SUPPORTED_FORMATS'), "SUPPORTED_FORMATS non défini"
        assert hasattr(config, 'MESSAGES'), "MESSAGES non défini"
        
        print("✅ Configuration valide")
        print(f"   📁 Dossier de téléchargement: {config.DOWNLOAD_PATH}")
        print(f"   📊 Taille max: {config.MAX_FILE_SIZE / 1024 / 1024:.0f} MB")
        print(f"   🎬 Formats supportés: {', '.join(config.SUPPORTED_FORMATS)}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def test_video_downloader():
    """Teste le module de téléchargement"""
    print("\n📥 Test du module de téléchargement...")
    
    try:
        from video_downloader import VideoDownloader
        
        # Créer une instance
        downloader = VideoDownloader()
        print("✅ Instance VideoDownloader créée")
        
        # Tester la validation d'URL
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4",
            "https://vimeo.com/123456789",
            "invalid_url",
            "not_a_url"
        ]
        
        for url in test_urls:
            is_valid = downloader._is_valid_url(url)
            status = "✅" if is_valid else "❌"
            print(f"   {status} {url}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur module de téléchargement: {e}")
        return False

def test_telegram_bot():
    """Teste le module du bot Telegram"""
    print("\n🤖 Test du module bot Telegram...")
    
    try:
        from telegram_bot import VideoUploaderBot
        
        # Créer une instance
        bot = VideoUploaderBot()
        print("✅ Instance VideoUploaderBot créée")
        
        # Tester l'extraction d'URLs
        test_texts = [
            "Voici une vidéo: https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://video.sibnet.ru/v/eb43c140e5f90c18644eb7b06981656e/4942633.mp4",
            "Pas d'URL ici",
            "https://example.com et https://test.com"
        ]
        
        for text in test_texts:
            urls = bot._extract_urls(text)
            print(f"   📝 '{text[:30]}...' -> {len(urls)} URL(s) trouvée(s)")
        
        return True
    except Exception as e:
        print(f"❌ Erreur module bot Telegram: {e}")
        return False

def test_dependencies():
    """Teste les dépendances"""
    print("\n📦 Test des dépendances...")
    
    dependencies = [
        ('python-telegram-bot', 'telegram'),
        ('aiohttp', 'aiohttp'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('yt-dlp', 'yt_dlp'),
    ]
    
    all_ok = True
    for package_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Non installé")
            all_ok = False
    
    return all_ok

def main():
    """Fonction principale de test"""
    print("🧪 Tests du Bot Telegram de Téléchargement de Vidéos")
    print("=" * 60)
    
    tests = [
        ("Importations", test_imports),
        ("Configuration", test_config),
        ("Module de téléchargement", test_video_downloader),
        ("Module bot Telegram", test_telegram_bot),
        ("Dépendances", test_dependencies),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé des tests:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Le bot est prêt à être utilisé.")
        print("\n📋 Prochaines étapes:")
        print("1. Configurez votre token de bot dans le fichier .env")
        print("2. Lancez le bot avec: python main.py")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Tests annulés par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1) 