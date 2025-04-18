import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
import os

# Thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("HexaCrypt 🔐")
root.geometry("500x450")

selected_file = None

# 🔐 Générer une clé depuis un mot de passe
def generate_key(password):
    hash_obj = hashlib.sha256(password.encode())
    return base64.urlsafe_b64encode(hash_obj.digest())

# 📄 Sauvegarder le mot de passe si option activée
def save_password(password):
    try:
        # Récupérer le dossier actuel du script (même dossier que le fichier .py ou l'exécutable)
        script_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_directory, "hexa_saved_passwords.txt")

        with open(file_path, "a") as f:
            f.write(f"{password}\n")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'enregistrer le mot de passe : {e}")

# 🔒 Chiffrer un fichier
def encrypt_file(path, password, delete_original, save_pw):
    try:
        key = generate_key(password)
        fernet = Fernet(key)

        with open(path, 'rb') as file:
            data = file.read()

        encrypted = fernet.encrypt(data)
        with open(path + ".hexacrypt", 'wb') as file:
            file.write(encrypted)

        if delete_original:
            os.remove(path)

        if save_pw:
            save_password(f"{os.path.basename(path)} | {password}")

        messagebox.showinfo("Succès", "Fichier chiffré avec succès ! 🔒")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du chiffrement : {e}")

# 🔓 Déchiffrer un fichier
def decrypt_file(path, password, delete_original):
    try:
        key = generate_key(password)
        fernet = Fernet(key)

        with open(path, 'rb') as file:
            data = file.read()

        decrypted = fernet.decrypt(data)

        output_path = path.replace(".hexacrypt", "")
        with open(output_path, 'wb') as file:
            file.write(decrypted)

        if delete_original:
            os.remove(path)

        messagebox.showinfo("Succès", "Fichier déchiffré avec succès ! 🔓")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du déchiffrement : {e}")

# 📂 Sélectionner un fichier
def select_file(action):
    file_path = filedialog.askopenfilename(title="Choisir un fichier", filetypes=[("All Files", "*.*")])
    if file_path:
        label_selected_file.configure(text=f"Fichier sélectionné : {file_path}")
        if action == "encrypt":
            btn_process.configure(
                command=lambda: encrypt_file(file_path, entry_password.get(), delete_var.get(), save_pw_var.get()),
                text="🔐 Chiffrer"
            )
        elif action == "decrypt":
            btn_process.configure(
                command=lambda: decrypt_file(file_path, entry_password.get(), delete_var.get()),
                text="🔓 Déchiffrer"
            )

# Widgets
label_selected_file = ctk.CTkLabel(root, text="Aucun fichier sélectionné", wraplength=480)
label_selected_file.pack(pady=10)

entry_password = ctk.CTkEntry(root, placeholder_text="Mot de passe", show="*")
entry_password.pack(pady=10)

delete_var = tk.BooleanVar()
chk_delete = ctk.CTkCheckBox(root, text="Supprimer le fichier original après l'opération", variable=delete_var)
chk_delete.pack(pady=5)

save_pw_var = tk.BooleanVar()
chk_save_pw = ctk.CTkCheckBox(root, text="Sauvegarder le mot de passe dans un .txt", variable=save_pw_var)
chk_save_pw.pack(pady=5)

btn_select_encrypt = ctk.CTkButton(root, text="📁 Sélectionner un fichier à chiffrer", command=lambda: select_file("encrypt"))
btn_select_encrypt.pack(pady=10)

btn_select_decrypt = ctk.CTkButton(root, text="📁 Sélectionner un fichier à déchiffrer", command=lambda: select_file("decrypt"))
btn_select_decrypt.pack(pady=5)

btn_process = ctk.CTkButton(root, text="🔒 Traitement", command=lambda: None, state="normal")
btn_process.pack(pady=20)

root.mainloop()
