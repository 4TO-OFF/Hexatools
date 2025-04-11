import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HexaPixel 🎨")
app.geometry("600x700")

original_image = None
working_image = None
revealed_pixels = set()
total_pixels = 0
canvas_img = None
canvas_img_id = None
canvas_size = 500

# 🧮 Adapter la taille sans déformer
def resize_keep_ratio(img, target_size):
    img_ratio = img.width / img.height
    canvas_ratio = target_size / target_size

    if img_ratio > canvas_ratio:
        new_width = target_size
        new_height = int(target_size / img_ratio)
    else:
        new_height = target_size
        new_width = int(target_size * img_ratio)

    return img.resize((new_width, new_height), Image.LANCZOS)

# 📂 Charger l'image
def load_image():
    global original_image, working_image, revealed_pixels, total_pixels
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_path:
        return

    original_image = Image.open(file_path).convert("RGB")
    working_image = Image.new("RGB", original_image.size, "black")
    revealed_pixels = set()
    total_pixels = original_image.width * original_image.height

    label_info.configure(text=f"Nombre de pixels : {total_pixels}")
    update_canvas()

# 🖼️ Affichage image
def update_canvas():
    global canvas_img, canvas_img_id
    img_resized = resize_keep_ratio(working_image, canvas_size)
    canvas_img = ImageTk.PhotoImage(img_resized)
    canvas.delete("all")
    canvas_img_id = canvas.create_image(canvas_size // 2, canvas_size // 2, anchor="center", image=canvas_img)

# 🎲 Révéler pixels
def reveal_pixels():
    global revealed_pixels, working_image

    if not original_image:
        return

    try:
        count = int(entry_count.get())
    except:
        return

    width, height = original_image.size
    max_reveal = min(count, total_pixels - len(revealed_pixels))
    revealed = 0

    while revealed < max_reveal:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if (x, y) not in revealed_pixels:
            color = original_image.getpixel((x, y))
            working_image.putpixel((x, y), color)
            revealed_pixels.add((x, y))
            revealed += 1

    update_canvas()
    percent = (len(revealed_pixels) / total_pixels) * 100
    label_percent.configure(text=f"Progression : {percent:.2f}%")

# 🔄 Reset
def reset_image():
    global working_image, revealed_pixels
    if not original_image:
        return
    working_image = Image.new("RGB", original_image.size, "black")
    revealed_pixels = set()
    update_canvas()
    label_percent.configure(text="Progression : 0.00%")

# === UI ===
btn_load = ctk.CTkButton(app, text="📂 Charger une image", command=load_image)
btn_load.pack(pady=10)

label_info = ctk.CTkLabel(app, text="Nombre de pixels : 0")
label_info.pack()

canvas = ctk.CTkCanvas(app, width=canvas_size, height=canvas_size, bg="black", highlightthickness=0)
canvas.pack(pady=10)

entry_count = ctk.CTkEntry(app, placeholder_text="Nombre de pixels à révéler")
entry_count.pack(pady=5)

btn_reveal = ctk.CTkButton(app, text="🔍 Révéler", command=reveal_pixels)
btn_reveal.pack(pady=5)

label_percent = ctk.CTkLabel(app, text="Progression : 0.00%")
label_percent.pack()

btn_reset = ctk.CTkButton(app, text="🔄 Réinitialiser", command=reset_image)
btn_reset.pack(pady=10)

app.mainloop()
