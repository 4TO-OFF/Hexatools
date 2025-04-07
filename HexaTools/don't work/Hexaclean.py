import os
import shutil
import ctypes
import subprocess
import sys  # N'oublions pas sys
import win32com.client
import tkinter as tk
from tkinter import messagebox

# Vérifier si le script a les droits admin
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Demander automatiquement les droits admin
def ask_admin_permission():
    if not is_admin():
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        messagebox.showerror("Erreur", "Ce script nécessite des droits administrateur. Relancez-le avec les droits administrateur !")
        script = sys.argv[0]
        subprocess.run(['runas', '/user:Administrator', script])  # Relancer le script avec les droits admin
        exit()  # Sortir si admin n'est pas accordé
    else:
        print("✅ Droits administrateur vérifiés.")

# Nettoyage des fichiers du navigateur
def clean_browser_cache():
    print("🧹 Suppression du cache des navigateurs...")
    browser_cache = [
        os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
        os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
        os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache')
    ]
    total_deleted = 0
    for cache in browser_cache:
        if os.path.exists(cache):
            total_deleted += clean_temp_folder(cache)
    return total_deleted

# Nettoyage des fichiers logs système
def clean_system_logs():
    print("📂 Suppression des fichiers logs système...")
    log_dirs = [
        "C:\\Windows\\Logs",
        "C:\\Windows\\Temp"
    ]
    total_deleted = 0
    for log_dir in log_dirs:
        total_deleted += clean_temp_folder(log_dir)
    return total_deleted

# Nettoyage des fichiers préchargés
def clean_prefetch():
    print("🗑️ Suppression des fichiers préchargés...")
    prefetch_dir = "C:\\Windows\\Prefetch"
    return clean_temp_folder(prefetch_dir)

# Nettoyage des fichiers de mise à jour de Windows
def clean_update_files():
    print("📁 Suppression des fichiers de mise à jour de Windows...")
    update_dir = "C:\\Windows\\SoftwareDistribution\\Download"
    return clean_temp_folder(update_dir)

# Nettoyage de la corbeille
def clean_recycle_bin():
    print("🗑️ Suppression des fichiers dans la corbeille...")
    shell = win32com.client.Dispatch("Shell.Application")
    for item in shell.NameSpace(10).Items():
        try:
            item.InvokeVerb("delete")
        except Exception as e:
            print(f"Erreur de suppression: {e}")
    return 0

# Nettoyer un dossier spécifique
def clean_temp_folder(folder):
    total_deleted = 0
    if not os.path.exists(folder):
        return total_deleted
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        for f in filenames:
            try:
                file_path = os.path.join(dirpath, f)
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                total_deleted += file_size
            except:
                pass
        for d in dirnames:
            try:
                shutil.rmtree(os.path.join(dirpath, d), ignore_errors=True)
            except:
                pass
    return total_deleted

# Obtenir la taille totale des fichiers d'un dossier
def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except:
                pass
    return total_size

# Convertir les octets en une unité lisible (Ko, Mo, Go)
def convert_size(size_bytes):
    for unit in ["o", "Ko", "Mo", "Go"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} To"

# Nettoyage principal
def run_cleaner():
    ask_admin_permission()  # Vérification du mode admin au démarrage

    temp_folders = [
        os.environ.get('TEMP', ''),
        "C:\\Windows\\Temp",
        "C:\\Windows\\SoftwareDistribution\\Download",
        "C:\\Windows\\Prefetch"
    ]
    total_size = sum(get_folder_size(folder) for folder in temp_folders if folder)

    print(f"📂 Espace pouvant être libéré : {convert_size(total_size)}")

    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    response = messagebox.askyesno("Confirmation", f"⚠️ Voulez-vous supprimer ces fichiers ?\nEspace à libérer: {convert_size(total_size)}")

    if response:  # Si l'utilisateur clique sur 'Oui'
        total_deleted = 0
        total_deleted += clean_browser_cache()
        total_deleted += clean_system_logs()
        total_deleted += clean_prefetch()
        total_deleted += clean_update_files()
        total_deleted += clean_recycle_bin()
        messagebox.showinfo("Succès", f"✅ Espace libéré : {convert_size(total_deleted)}")
    else:
        messagebox.showinfo("Annulé", "🚫 Nettoyage annulé.")

# Lancer le nettoyeur
if __name__ == "__main__":
    run_cleaner()
