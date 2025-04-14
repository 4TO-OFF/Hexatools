import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import io
import base64

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HexaHide 🫥")
app.geometry("600x700")

# Fonctions utilitaires

def hide_text_in_image(image_path, message, output_path):
    img = Image.open(image_path)
    encoded = message.encode("utf-8")
    b64 = base64.b64encode(encoded).decode("utf-8")
    if len(b64) > img.width * img.height:
        raise ValueError("Message trop long pour l'image")
    pixels = img.load()
    i = 0
    for y in range(img.height):
        for x in range(img.width):
            if i < len(b64):
                r, g, b = pixels[x, y]
                pixels[x, y] = (ord(b64[i]), g, b)
                i += 1
    img.save(output_path)

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    chars = []
    for y in range(img.height):
        for x in range(img.width):
            r, _, _ = pixels[x, y]
            if r == 0:
                break
            chars.append(chr(r))
    try:
        decoded = base64.b64decode("".join(chars)).decode("utf-8")
    except:
        decoded = "Erreur de décodage."
    return decoded

def hide_file_in_image(image_path, file_path, output_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64_data = base64.b64encode(data).decode("utf-8")
    img = Image.open(image_path)
    if len(b64_data) > img.width * img.height:
        raise ValueError("Fichier trop grand pour l'image")
    pixels = img.load()
    i = 0
    for y in range(img.height):
        for x in range(img.width):
            if i < len(b64_data):
                r, g, b = pixels[x, y]
                pixels[x, y] = (ord(b64_data[i]), g, b)
                i += 1
    img.save(output_path)

def extract_file_from_image(image_path, output_path):
    img = Image.open(image_path)
    pixels = img.load()
    chars = []
    for y in range(img.height):
        for x in range(img.width):
            r, _, _ = pixels[x, y]
            if r == 0:
                break
            chars.append(chr(r))
    try:
        data = base64.b64decode("".join(chars))
        with open(output_path, "wb") as f:
            f.write(data)
        return True
    except:
        return False

# === UI ===
label = ctk.CTkLabel(app, text="Choisis une option ⬇️")
label.pack(pady=10)

entry_text = ctk.CTkEntry(app, placeholder_text="Message à cacher")
entry_text.pack(pady=5)

btn_hide_text = ctk.CTkButton(app, text="📥 Cacher un message texte", command=lambda: hide_text_ui())
btn_hide_text.pack(pady=5)

def hide_text_ui():
    img = filedialog.askopenfilename(title="Image support")
    if not img: return
    out = filedialog.asksaveasfilename(defaultextension=".png")
    if not out: return
    try:
        hide_text_in_image(img, entry_text.get(), out)
        messagebox.showinfo("Succès", "Message caché avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn_extract_text = ctk.CTkButton(app, text="📤 Extraire un message texte", command=lambda: extract_text_ui())
btn_extract_text.pack(pady=5)

def extract_text_ui():
    img = filedialog.askopenfilename(title="Image avec message")
    if not img: return
    msg = extract_text_from_image(img)
    messagebox.showinfo("Message caché", msg)

btn_hide_file = ctk.CTkButton(app, text="📁 Cacher un fichier", command=lambda: hide_file_ui())
btn_hide_file.pack(pady=5)

def hide_file_ui():
    img = filedialog.askopenfilename(title="Image support")
    if not img: return
    file = filedialog.askopenfilename(title="Fichier à cacher")
    if not file: return
    out = filedialog.asksaveasfilename(defaultextension=".png")
    if not out: return
    try:
        hide_file_in_image(img, file, out)
        messagebox.showinfo("Succès", "Fichier caché avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn_extract_file = ctk.CTkButton(app, text="🗂️ Extraire un fichier", command=lambda: extract_file_ui())
btn_extract_file.pack(pady=5)

def extract_file_ui():
    img = filedialog.askopenfilename(title="Image contenant un fichier")
    if not img: return
    out = filedialog.asksaveasfilename(title="Enregistrer le fichier")
    if not out: return
    if extract_file_from_image(img, out):
        messagebox.showinfo("Succès", "Fichier extrait avec succès")
    else:
        messagebox.showerror("Erreur", "Impossible d'extraire le fichier")

app.mainloop()
