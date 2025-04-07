import tkinter as tk
import customtkinter as ctk
import hashlib
import time
from tkinter import filedialog

# 🌑 Thème sombre
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ✅ Fonction de complexification avancée
def complexify_password():
    password = entry_password.get()
    if not password:
        strength_label.configure(text="❌ Entrez un mot de passe d'abord.")
        return

    substitutions = {
        "a": "@", "e": "€", "i": "1", "o": "0", "s": "$", "l": "1"
    }
    special_chars = "!@#$%^&*()_+-=[]{}|;:'\"<>,./?"
    complexified = ""

    for i, char in enumerate(password):
        lower_char = char.lower()

        if lower_char in substitutions:
            complexified += substitutions[lower_char]
            continue

        if lower_char == "u":
            prev_char = password[i-1] if i > 0 else ""
            next_char = password[i+1] if i < len(password) - 1 else ""

            u_transformed = "U" if prev_char in special_chars else "u"
            if next_char.isdigit():
                u_transformed += "_"
            complexified += u_transformed
            continue

        complexified += char

    entry_password.delete(0, tk.END)
    entry_password.insert(0, complexified)
    strength_label.configure(text="⚙️ Mot de passe complexifié !")

# 🛡 Fonction de vérification de la robustesse
def check_password_strength():
    password = entry_password.get()
    length = len(password)

    score = 0
    feedback = []

    # Longueur
    if length >= 12:
        score += 2
        feedback.append("📏 Longueur : Très bonne")
    elif length >= 8:
        score += 1
        feedback.append("📏 Longueur : Correcte")
    else:
        feedback.append("📏 Longueur : Trop courte")

    # Complexité
    has_digit = any(c.isdigit() for c in password)
    has_alpha = any(c.isalpha() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:'\"<>,./?" for c in password)

    if has_digit and has_alpha and has_special:
        score += 2
        feedback.append("🧩 Complexité : Très bonne")
    elif (has_digit and has_alpha) or (has_alpha and has_special):
        score += 1
        feedback.append("🧩 Complexité : Moyenne")
    else:
        feedback.append("🧩 Complexité : Faible")

    # Estimation force brute
    combinations = 94 ** length
    time_to_crack = combinations / (1e9)  # 1 milliard essais/sec
    if time_to_crack >= 1e6:
        score += 2
        feedback.append("⏳ Temps estimé : Très long")
    elif time_to_crack >= 1e3:
        score += 1
        feedback.append("⏳ Temps estimé : Moyen")
    else:
        feedback.append("⏳ Temps estimé : Court")

    # Score final
    feedback.append(f"🔢 Score final : {score}/6")
    result = "\n".join(feedback)

    strength_label.configure(text=result)

# 🧑‍💻 Fonction brute force avec dictionnaire
def brute_force_test():
    password = entry_password.get()
    found = False

    file_path = filedialog.askopenfilename(title="Choisir un fichier de mots de passe", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        result_label.configure(text="❌ Aucun fichier sélectionné.")
        return

    try:
        with open(file_path, "r", encoding="latin-1") as file:
            start_time = time.time()
            for line in file:
                line = line.strip()
                if hashlib.md5(line.encode('utf-8')).hexdigest() == hashlib.md5(password.encode('utf-8')).hexdigest():
                    found = True
                    break
            end_time = time.time()

            if found:
                result_label.configure(text=f"🔓 Mot de passe trouvé dans {end_time - start_time:.2f} sec")
            else:
                result_label.configure(text="🔒 Mot de passe non trouvé dans le dictionnaire.")
    except Exception as e:
        result_label.configure(text=f"❌ Erreur : {str(e)}")

# 👁️ Afficher/masquer mot de passe
def toggle_password_visibility():
    entry_password.configure(show="" if var_show_password.get() else "*")

# 🎛️ Interface
root = ctk.CTk()
root.title("HexaPass - Test de mot de passe")
root.geometry("500x600")

label_password = ctk.CTkLabel(root, text="🔐 Entrez un mot de passe :")
label_password.pack(pady=10)

entry_password = ctk.CTkEntry(root, show="*", width=300)
entry_password.pack(pady=5)

var_show_password = tk.BooleanVar()
check_show_password = ctk.CTkCheckBox(root, text="Afficher le mot de passe", variable=var_show_password, command=toggle_password_visibility)
check_show_password.pack(pady=10)

btn_check_strength = ctk.CTkButton(root, text="Vérifier la robustesse", command=check_password_strength)
btn_check_strength.pack(pady=10)

btn_complexify = ctk.CTkButton(root, text="Complexifier automatiquement", command=complexify_password)
btn_complexify.pack(pady=10)

strength_label = ctk.CTkLabel(root, text="Force du mot de passe :")
strength_label.pack(pady=10)

btn_bruteforce = ctk.CTkButton(root, text="Tester avec brute force (fichier)", command=brute_force_test)
btn_bruteforce.pack(pady=10)

result_label = ctk.CTkLabel(root, text="Résultats :")
result_label.pack(pady=10)

# ▶️ Lancer
root.mainloop()
