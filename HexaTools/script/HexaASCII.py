import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HexaASCII 🎨")
app.geometry("1100x600")

ascii_chars = "@%#*+=-:. "
font = ImageFont.truetype("arial.ttf", 10)  # Utilise une police monospace dispo
original_image = None
ascii_image = None
quality = 3  # Qualité par défaut

# 🧮 Adapter taille sans déformation
def resize_keep_ratio(img, new_width=100):
    width, height = img.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return img.resize((new_width, new_height))

# 🎨 Convertir en ASCII couleur avec qualité ajustée
def convert_to_ascii_color(img, quality):
    img = resize_keep_ratio(img, new_width=120)
    img = img.convert("RGB")

    width, height = img.size
    ascii_img = Image.new("RGB", (width * 10, height * 10), color="black")
    draw = ImageDraw.Draw(ascii_img)

    # Ajustement de la qualité
    scale_factor = max(1, 6 - quality)  # Plus le quality est bas, plus les pixels sont grands
    for y in range(0, height, scale_factor):
        for x in range(0, width, scale_factor):
            r, g, b = img.getpixel((x, y))
            gray = int((r + g + b) / 3)
            char = ascii_chars[int(gray / 256 * len(ascii_chars)) - 1]
            draw.text((x * 10, y * 10), char, font=font, fill=(r, g, b))

    return ascii_img

# 📂 Choisir une image
def load_image():
    global original_image, ascii_image
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    original_image = Image.open(file_path)
    ascii_image = None
    update_preview()

# 🔁 Convertir
def convert():
    global ascii_image
    if original_image:
        ascii_image = convert_to_ascii_color(original_image, quality)
        update_preview()

# 💾 Télécharger
def save_ascii():
    if ascii_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            ascii_image.save(file_path)

# 🖼️ Mettre à jour les aperçus
def update_preview():
    if original_image:
        img1 = original_image.copy()
        img1.thumbnail((400, 400))
        img1 = ctk.CTkImage(dark_image=img1, size=img1.size)
        label_original.configure(image=img1)
        label_original.image = img1
    if ascii_image:
        img2 = ascii_image.copy()
        img2.thumbnail((400, 400))
        img2 = ctk.CTkImage(dark_image=img2, size=img2.size)
        label_ascii.configure(image=img2)
        label_ascii.image = img2

# 🎯 Mise à jour de la qualité
def update_quality(value):
    global quality
    quality = int(value)
    label_quality.configure(text=f"Qualité : {quality}")

# === UI ===
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

btn_load = ctk.CTkButton(frame, text="📂 Choisir une image", command=load_image)
btn_load.grid(row=0, column=0, padx=10)

btn_convert = ctk.CTkButton(frame, text="🔁 Convertir en ASCII", command=convert)
btn_convert.grid(row=0, column=1, padx=10)

btn_save = ctk.CTkButton(frame, text="💾 Télécharger", command=save_ascii)
btn_save.grid(row=0, column=2, padx=10)

label_original = ctk.CTkLabel(app, text="Image originale")
label_original.pack(side="left", padx=10)

label_ascii = ctk.CTkLabel(app, text="Image ASCII")
label_ascii.pack(side="right", padx=10)

# Curseur de qualité
label_quality = ctk.CTkLabel(app, text="Qualité : 3")
label_quality.pack(pady=10)

quality_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=4, command=update_quality)
quality_slider.set(3)
quality_slider.pack(pady=10)

app.mainloop()
