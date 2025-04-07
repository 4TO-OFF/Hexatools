import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os
import magic
from tqdm import tqdm

# Ta clé API VirusTotal (remplace "VOTRE_CLE_API" par ta clé réelle)
API_KEY = "VOTRE_CLE_API"
URL = "https://www.virustotal.com/api/v3/files/"

# Fonction pour vérifier un fichier avec VirusTotal
def scan_with_virustotal(file_path):
    try:
        # Ouvrir le fichier et l'envoyer à VirusTotal
        with open(file_path, "rb") as f:
            files = {
                'file': (os.path.basename(file_path), f),
            }
            headers = {
                "x-apikey": API_KEY
            }

            # Envoi du fichier à VirusTotal pour l'analyser
            response = requests.post(URL, files=files, headers=headers)
            
            if response.status_code == 200:
                json_response = response.json()
                if json_response.get('data'):
                    analysis_results = json_response['data']['attributes']['last_analysis_stats']
                    if analysis_results['malicious'] > 0:
                        return True  # Virus trouvé
                    else:
                        return False  # Aucun virus détecté
                else:
                    return None  # Résultats non disponibles
            else:
                print(f"Erreur lors de l'analyse avec VirusTotal : {response.status_code}")
                return None

    except Exception as e:
        print(f"Erreur : {e}")
        return None

# Fonction d'analyse de fichier avec message
def analyze_file():
    file_path = filedialog.askopenfilename(title="Sélectionner un fichier à analyser")
    if file_path:
        print(f"🔍 Analyse du fichier : {file_path}")
        result = scan_with_virustotal(file_path)
        
        if result is None:
            messagebox.showinfo("Résultat inconnu", "Impossible d'obtenir une analyse à partir de VirusTotal.")
        elif result:
            messagebox.showwarning("Virus détecté", "Ce fichier a été détecté comme un virus par VirusTotal !")
        else:
            messagebox.showinfo("Fichier sécurisé", "Aucun virus détecté dans ce fichier.")

# Fonction d'analyse de dossier
def analyze_folder():
    folder_path = filedialog.askdirectory(title="Sélectionner un dossier à analyser")
    if folder_path:
        print(f"🔍 Analyse du dossier : {folder_path}")
        
        # Créer une barre de progression
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            messagebox.showinfo("Aucun fichier", "Le dossier ne contient aucun fichier.")
            return
        
        # Initialisation de la barre de progression
        progress = tqdm(files, desc="Analyse des fichiers", unit="fichier")
        for file_name in progress:
            file_path = os.path.join(folder_path, file_name)
            result = scan_with_virustotal(file_path)

            if result is None:
                progress.set_postfix(status="Résultats inconnus")
            elif result:
                progress.set_postfix(status="Virus détecté")
            else:
                progress.set_postfix(status="Fichier sécurisé")

        messagebox.showinfo("Analyse terminée", "L'analyse du dossier est terminée.")

# Interface Tkinter
root = tk.Tk()
root.title("HexaScan - Scanner de fichiers et dossiers")
root.geometry("400x200")

# Boutons
analyze_file_btn = tk.Button(root, text="Analyser un fichier", command=analyze_file)
analyze_file_btn.pack(pady=10)

analyze_folder_btn = tk.Button(root, text="Analyser un dossier", command=analyze_folder)
analyze_folder_btn.pack(pady=10)

# Lancer l'interface
root.mainloop()
