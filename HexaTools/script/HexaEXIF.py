import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from PIL.ExifTags import TAGS

# 🎨 Apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 📦 Fenêtre principale
app = ctk.CTk()
app.title("🕵️ Metadata Viewer")
app.geometry("700x500")

# 🧠 Fonction pour lire les EXIF
def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if not info:
        return exif_data
    for tag, value in info.items():
        tagname = TAGS.get(tag, tag)
        exif_data[tagname] = value
    return exif_data

# 📂 Sélection de l’image
def select_image():
    path = filedialog.askopenfilename(title="Choisir une image", filetypes=[("Images", "*.jpg *.jpeg *.png")])
    if not path:
        return
    try:
        img = Image.open(path)
        exif = get_exif_data(img)
        output.configure(state="normal")
        output.delete("1.0", "end")
        if not exif:
            output.insert("end", "❌ Aucune métadonnée EXIF trouvée.")
        else:
            for tag, value in exif.items():
                output.insert("end", f"{tag} : {value}\n")
        output.configure(state="disabled")
    except Exception as e:
        output.insert("end", f"Erreur : {e}")

# 📌 UI
title = ctk.CTkLabel(app, text="🕵️ Metadata Viewer", font=("Arial", 24))
title.pack(pady=15)

select_btn = ctk.CTkButton(app, text="📂 Sélectionner une image", command=select_image)
select_btn.pack(pady=10)

output = ctk.CTkTextbox(app, width=650, height=350)
output.pack(pady=10)
output.configure(state="disabled")

# 🚀 Start
app.mainloop()
