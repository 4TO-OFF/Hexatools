import os
import sys
import subprocess
import customtkinter as ctk
import tkinter as tk

# 🎨 Apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 📁 Dossier des outils
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
TOOLS_FOLDER = os.path.join(BASE_DIR, "script")

# 📦 Fenêtre principale
app = ctk.CTk()
app.title("HexaTools 🚀 Launcher")
app.geometry("500x600")

# 🧩 Titre
title = ctk.CTkLabel(app, text="🎛️ HexaTools Launcher", font=("Arial", 24))
title.pack(pady=20)

# 📂 Charger les outils
tools = []
for file in os.listdir(TOOLS_FOLDER):
    if file.endswith(".py"):
        tool_name = file.replace(".py", "")
        tools.append((tool_name, os.path.join(TOOLS_FOLDER, file)))

# 📄 Liste des outils
frame = ctk.CTkScrollableFrame(app, width=460, height=400)
frame.pack(pady=10)

def launch_tool(path):
    subprocess.Popen(["python", path])

for name, path in tools:
    btn = ctk.CTkButton(frame, text=f"▶️ {name}", command=lambda p=path: launch_tool(p))
    btn.pack(pady=5, padx=10, fill="x")

# 🖼️ Footer
footer = ctk.CTkLabel(app, text="Made by 4TO-OFF 💻", font=("Arial", 12))
footer.pack(pady=10)

# 🧠 Start
app.mainloop()
