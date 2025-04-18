import customtkinter as ctk
import os
import stat
import mimetypes
from tkinter import filedialog
from datetime import datetime

# 🌙 Thème sombre
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 📦 App
app = ctk.CTk()
app.title("HexaInfo - Analyse de fichier")
app.geometry("600x500")

# 🔍 Analyse
def analyze_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        stats = os.stat(file_path)
        size = stats.st_size
        created = datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        # Type MIME + signature simplifiée
        mime_type, _ = mimetypes.guess_type(file_path)
        file_type = mime_type if mime_type else "Inconnu"

        # Permissions
        perms = ""
        perms += "Lecture ✅\n" if bool(stats.st_mode & stat.S_IRUSR) else "Lecture ❌\n"
        perms += "Écriture ✅\n" if bool(stats.st_mode & stat.S_IWUSR) else "Écriture ❌\n"
        perms += "Exécution ✅" if bool(stats.st_mode & stat.S_IXUSR) else "Exécution ❌"

        result_label.configure(
            text=f"""
📄 Fichier : {os.path.basename(file_path)}
📁 Chemin : {file_path}
📐 Taille : {size} octets
📅 Créé le : {created}
♻️ Modifié le : {modified}
🔍 Type : {file_type}
🛡 Permissions :
{perms}
            """
        )
    except Exception as e:
        result_label.configure(text=f"Erreur : {str(e)}")

# 🎛️ UI
title = ctk.CTkLabel(app, text="HexaInfo", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=20)

btn_select = ctk.CTkButton(app, text="📂 Sélectionner un fichier", command=analyze_file)
btn_select.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", justify="left", anchor="w", width=550)
result_label.pack(pady=20)

# 🚀 Start
app.mainloop()
