import os
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime

# ⚙️ Setup UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HexaFind - Recherche de fichiers")
app.geometry("700x550")

# 📁 Sélection dossier
def choisir_dossier():
    dossier = filedialog.askdirectory()
    entry_dossier.delete(0, tk.END)
    entry_dossier.insert(0, dossier)

# 🔍 Recherche
def lancer_recherche():
    dossier_base = entry_dossier.get()
    nom_fichier = entry_nom.get().lower().strip()
    extension = entry_extension.get().lower().strip()
    taille_min = entry_taille_min.get()
    date_min = entry_date.get()
    exclure_windows = bool(var_exclure_windows.get())

    results_box.delete(0, tk.END)

    if not os.path.exists(dossier_base):
        messagebox.showerror("Erreur", "Chemin invalide.")
        return

    try:
        taille_min = int(taille_min) * 1024 if taille_min else 0
    except ValueError:
        taille_min = 0

    try:
        timestamp_min = time.mktime(datetime.strptime(date_min, "%d/%m/%Y").timetuple()) if date_min else 0
    except ValueError:
        timestamp_min = 0

    for root, dirs, files in os.walk(dossier_base):
        if exclure_windows and "Windows" in root:
            continue

        for file in files:
            path = os.path.join(root, file)
            try:
                if nom_fichier and nom_fichier not in file.lower():
                    continue

                if extension and not file.lower().endswith(extension):
                    continue

                if os.path.getsize(path) < taille_min:
                    continue

                if os.path.getmtime(path) < timestamp_min:
                    continue

                results_box.insert(tk.END, path)
            except:
                pass

# 📂 Ouvrir le fichier sélectionné
def open_selected_file(event=None):
    selection = results_box.curselection()
    if selection:
        os.startfile(results_box.get(selection[0]))

# 🧠 Interface
frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

entry_dossier = ctk.CTkEntry(frame, placeholder_text="Dossier de base")
entry_dossier.pack(fill="x", pady=5)

btn_parcourir = ctk.CTkButton(frame, text="📁 Parcourir", command=choisir_dossier)
btn_parcourir.pack(pady=5)

entry_nom = ctk.CTkEntry(frame, placeholder_text="Nom du fichier (partiel ou complet)")
entry_nom.pack(fill="x", pady=5)

entry_extension = ctk.CTkEntry(frame, placeholder_text="Extension (ex: .mp4)")
entry_extension.pack(fill="x", pady=5)

entry_taille_min = ctk.CTkEntry(frame, placeholder_text="Taille min (en Ko)")
entry_taille_min.pack(fill="x", pady=5)

entry_date = ctk.CTkEntry(frame, placeholder_text="Date min (JJ/MM/AAAA)")
entry_date.pack(fill="x", pady=5)

var_exclure_windows = ctk.CTkCheckBox(frame, text="Exclure les dossiers système (ex: Windows)")
var_exclure_windows.pack(pady=5)

btn_rechercher = ctk.CTkButton(frame, text="🔍 Rechercher", command=lancer_recherche)
btn_rechercher.pack(pady=10)

# Résultats
frame_listbox = ctk.CTkFrame(frame)
frame_listbox.pack(fill="both", expand=True, pady=5)

scrollbar = tk.Scrollbar(frame_listbox)
scrollbar.pack(side="right", fill="y")

results_box = tk.Listbox(frame_listbox, height=15, yscrollcommand=scrollbar.set, bg="#1a1a1a", fg="white", selectbackground="#007fff")
results_box.pack(fill="both", expand=True)

scrollbar.config(command=results_box.yview)
results_box.bind("<Double-1>", open_selected_file)

app.mainloop()
