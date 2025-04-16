import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from customtkinter import CTkImage
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HexaCompressor")
app.geometry("500x550")

def select_image():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")]
    )
    if filepath:
        image_path_label.configure(text=filepath)
        compress_button.configure(state="normal")
        show_preview(filepath)

def compress_image():
    path = image_path_label.cget("text")
    quality = int(quality_slider.get())
    if path:
        try:
            img = Image.open(path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            filename, ext = os.path.splitext(os.path.basename(path))
            new_filename = f"{filename}_hexacompressed.jpg"
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile=new_filename)

            if save_path:
                img.save(save_path, "JPEG", quality=quality)
                status_label.configure(text=f"✅ Sauvegardé sous : {new_filename}")
        except Exception as e:
            status_label.configure(text=f"❌ Erreur : {str(e)}")

def update_quality_label(value):
    value = int(value)
    quality_value.configure(text=f"{value} %")

def show_preview(path):
    try:
        img = Image.open(path)
        img.thumbnail((300, 300))
        tk_image = CTkImage(light_image=img, size=img.size)
        preview_label.configure(image=tk_image, text="")
        preview_label.image = tk_image
    except Exception as e:
        status_label.configure(text=f"⚠️ Erreur preview : {str(e)}")

# UI
title = ctk.CTkLabel(app, text="HexaCompressor", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(pady=10)

select_button = ctk.CTkButton(app, text="Sélectionner une image", command=select_image)
select_button.pack(pady=10)

image_path_label = ctk.CTkLabel(app, text="Aucune image sélectionnée", wraplength=480)
image_path_label.pack(pady=5)

preview_label = ctk.CTkLabel(app, text="Prévisualisation")
preview_label.pack(pady=10)

quality_slider = ctk.CTkSlider(app, from_=1, to=100, number_of_steps=99, command=update_quality_label)
quality_slider.set(60)
quality_slider.pack(pady=5)

quality_value = ctk.CTkLabel(app, text="60 %")
quality_value.pack()

legend_label = ctk.CTkLabel(app, text="100 % = Qualité max / 1 % = Très compressé", font=ctk.CTkFont(size=11))
legend_label.pack()

compress_button = ctk.CTkButton(app, text="Compresser et enregistrer", command=compress_image, state="disabled")
compress_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

app.mainloop()
