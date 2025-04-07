import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import qrcode

# Thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App
app = ctk.CTk()
app.title("HexaQR - Générateur de QR Code")
app.geometry("500x600")

qr_img = None  # Stock l'image QR brut (PIL)
qr_img_ctk = None  # Stock l'image QR en CTkImage

# 🔃 Génération du QR
def generate_qr():
    global qr_img, qr_img_ctk
    data = entry_text.get()

    if not data:
        qr_label.configure(image=None)
        qr_label.image = None
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    preview = qr_img.resize((250, 250))

    qr_img_ctk = ctk.CTkImage(light_image=preview, dark_image=preview, size=(250, 250))
    qr_label.configure(image=qr_img_ctk)
    qr_label.image = qr_img_ctk

# 💾 Enregistrement
def save_qr():
    if qr_img:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if file_path:
            qr_img.save(file_path)

# 🎛 Interface
entry_text = ctk.CTkEntry(app, placeholder_text="Texte ou URL à encoder", width=400)
entry_text.pack(pady=20)

btn_generate = ctk.CTkButton(app, text="Générer le QR Code", command=generate_qr)
btn_generate.pack(pady=10)

qr_label = ctk.CTkLabel(app, text="")
qr_label.pack(pady=20)

btn_save = ctk.CTkButton(app, text="Enregistrer le QR Code", command=save_qr)
btn_save.pack(pady=10)

app.mainloop()
