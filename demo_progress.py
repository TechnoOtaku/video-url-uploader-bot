#!/usr/bin/env python3
"""
Script de démonstration des fonctionnalités de progression
"""

import asyncio
import time
import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from video_downloader import VideoDownloader

def simulate_progress():
    """Simule une progression de téléchargement pour démontrer les fonctionnalités"""
    print("🎬 Démonstration des fonctionnalités de progression")
    print("=" * 60)
    
    downloader = VideoDownloader()
    user_id = 12345  # ID utilisateur fictif
    
    # Simuler les données de progression
    progress_data = [
        {'percentage': 0, 'downloaded_mb': 0, 'total_mb': 25.5, 'speed_mb': 0, 'eta': 'Calcul...'},
        {'percentage': 5, 'downloaded_mb': 1.3, 'total_mb': 25.5, 'speed_mb': 2.1, 'eta': '12m 30s'},
        {'percentage': 15, 'downloaded_mb': 3.8, 'total_mb': 25.5, 'speed_mb': 2.5, 'eta': '8m 45s'},
        {'percentage': 30, 'downloaded_mb': 7.7, 'total_mb': 25.5, 'speed_mb': 2.8, 'eta': '6m 20s'},
        {'percentage': 50, 'downloaded_mb': 12.8, 'total_mb': 25.5, 'speed_mb': 3.1, 'eta': '4m 10s'},
        {'percentage': 70, 'downloaded_mb': 17.9, 'total_mb': 25.5, 'speed_mb': 3.3, 'eta': '2m 25s'},
        {'percentage': 85, 'downloaded_mb': 21.7, 'total_mb': 25.5, 'speed_mb': 3.5, 'eta': '1m 8s'},
        {'percentage': 95, 'downloaded_mb': 24.2, 'total_mb': 25.5, 'speed_mb': 3.2, 'eta': '0m 25s'},
        {'percentage': 100, 'downloaded_mb': 25.5, 'total_mb': 25.5, 'speed_mb': 0, 'eta': 'Terminé'},
    ]
    
    print("📥 Simulation d'un téléchargement de 25.5 MB")
    print("⏳ Démarrage de la simulation...\n")
    
    for i, data in enumerate(progress_data):
        # Stocker les données de progression
        downloader.download_progress[user_id] = data
        
        # Afficher le message formaté
        message = downloader.format_progress_message(user_id)
        print(f"🔄 Étape {i+1}/{len(progress_data)}:")
        print(message)
        print("-" * 60)
        
        # Attendre un peu pour simuler le temps réel
        if i < len(progress_data) - 1:
            time.sleep(1)
    
    print("✅ Simulation terminée !")
    print("\n📋 Fonctionnalités démontrées:")
    print("• 📊 Barre de progression visuelle")
    print("• ⚡ Affichage de la vitesse en temps réel")
    print("• ⏱️ Estimation du temps restant")
    print("• 📁 Informations détaillées sur le fichier")
    print("• 🔄 Mise à jour automatique toutes les 2 secondes")

def test_formatting_functions():
    """Teste les fonctions de formatage"""
    print("\n🔧 Test des fonctions de formatage")
    print("=" * 40)
    
    downloader = VideoDownloader()
    
    # Test du formatage du temps
    test_times = [0, 30, 90, 3600, 7325, None, -1]
    print("⏱️ Formatage du temps:")
    for seconds in test_times:
        formatted = downloader._format_time(seconds)
        print(f"   {seconds}s -> {formatted}")
    
    # Test du formatage de la taille
    test_sizes = [512, 1024, 1024*1024, 25*1024*1024, 1024*1024*1024]
    print("\n📁 Formatage de la taille:")
    for size in test_sizes:
        formatted = downloader._format_size(size)
        print(f"   {size} bytes -> {formatted}")

def main():
    """Fonction principale"""
    try:
        # Test des fonctions de formatage
        test_formatting_functions()
        
        # Simulation de progression
        simulate_progress()
        
        print("\n🎉 Démonstration terminée avec succès !")
        print("\n💡 Pour tester avec un vrai bot Telegram:")
        print("1. Configurez votre token dans le fichier .env")
        print("2. Lancez: python main.py")
        print("3. Envoyez un lien vidéo au bot")
        
    except KeyboardInterrupt:
        print("\n\n👋 Démonstration annulée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")

if __name__ == "__main__":
    main() 