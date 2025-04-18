import customtkinter as ctk
from tkinter import filedialog
import hashlib

# 🎨 Apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 🪟 App
app = ctk.CTk()
app.title("🔐 HexaHash")
app.geometry("700x600")

# 🧠 Hash functions
def compute_hashes(file_path):
    try:
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                md5.update(chunk)
                sha1.update(chunk)
                sha256.update(chunk)

        return {
            "MD5": md5.hexdigest(),
            "SHA-1": sha1.hexdigest(),
            "SHA-256": sha256.hexdigest()
        }

    except Exception as e:
        return {"Erreur": str(e)}

# 📂 Sélectionner fichier
def select_file():
    path = filedialog.askopenfilename(title="Choisir un fichier")
    if not path:
        return

    result = compute_hashes(path)
    output.configure(state="normal")
    output.delete("1.0", "end")

    for algo, hash_value in result.items():
        output.insert("end", f"{algo} : {hash_value}\n")

    output.configure(state="disabled")

    # Vérification si hash donné
    check_hash_match(result)

# ✅ Vérifier si le hash entré correspond
def check_hash_match(result):
    user_hash = hash_entry.get().strip().lower()
    if not user_hash:
        result_label.configure(text="🔍 Aucune vérification de hash", text_color="gray")
        return

    for algo, hash_value in result.items():
        if user_hash == hash_value.lower():
            result_label.configure(text=f"✅ Match avec {algo}", text_color="green")
            return

    result_label.configure(text="❌ Aucune correspondance trouvée", text_color="red")

# 🔘 UI
title = ctk.CTkLabel(app, text="🔐 HexaHash", font=("Arial", 24))
title.pack(pady=15)

select_btn = ctk.CTkButton(app, text="📂 Sélectionner un fichier", command=select_file)
select_btn.pack(pady=10)

output = ctk.CTkTextbox(app, width=650, height=280)
output.pack(pady=10)
output.configure(state="disabled")

hash_entry = ctk.CTkEntry(app, placeholder_text="✏️ Entrer un hash à vérifier (MD5, SHA-1, SHA-256)...", width=650)
hash_entry.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
result_label.pack(pady=5)

# 🚀 Start
app.mainloop()
