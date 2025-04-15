import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import imageio
import soundfile as sf
import os

# Setup de l'application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎧 HexaConvert v1.1")
app.geometry("600x350")
app.resizable(False, False)

# Liste des formats compatibles
image_formats = ".png, .jpg, .jpeg, .bmp, .gif"
audio_formats = ".wav, .flac, .ogg, .aiff"
video_formats = ".mp4, .avi, .mov, .mkv, .webm"

def select_file():
    """Ouvre une boîte de dialogue pour sélectionner un fichier"""
    filepath = filedialog.askopenfilename()
    if filepath:
        entry_file.delete(0, ctk.END)
        entry_file.insert(0, filepath)


def convert():
    """Fonction de conversion de fichier selon son type"""
    input_path = entry_file.get()
    output_format = entry_format.get().lower().strip()

    # Vérifier si les champs sont remplis
    if not input_path or not output_format:
        messagebox.showerror("Erreur", "Merci de remplir tous les champs.")
        return

    ext = os.path.splitext(input_path)[1].lower()
    output_path = os.path.splitext(input_path)[0] + '.' + output_format

    try:
        # Conversion d'image
        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            img = Image.open(input_path)

            # Conversion RGBA -> RGB pour les JPEG
            if output_format in ['jpg', 'jpeg'] and img.mode == 'RGBA':
                img = img.convert('RGB')

            img.save(output_path)
            messagebox.showinfo("✅ Succès", f"Image convertie → {output_path}")

        # Conversion d'audio
        elif ext in ['.wav', '.flac', '.ogg', '.aiff']:
            data, samplerate = sf.read(input_path)
            sf.write(output_path, data, samplerate)
            messagebox.showinfo("✅ Succès", f"Audio converti → {output_path}")

        # Conversion de vidéo
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            reader = imageio.get_reader(input_path)
            writer = imageio.get_writer(output_path, fps=reader.get_meta_data()['fps'])

            for frame in reader:
                writer.append_data(frame)
            reader.close()
            writer.close()
            messagebox.showinfo("✅ Succès", f"Vidéo convertie → {output_path}")

        else:
            messagebox.showerror("❌ Erreur", "Format non pris en charge.")

    except Exception as e:
        messagebox.showerror("💥 Exception", str(e))


# Interface utilisateur
ctk.CTkLabel(app, text="Fichier à convertir:").pack(pady=(20, 4))
entry_file = ctk.CTkEntry(app, width=340)
entry_file.pack()
ctk.CTkButton(app, text="📁 Parcourir", command=select_file).pack(pady=6)

ctk.CTkLabel(app, text="Format de sortie (ex: jpg, mp4, wav):").pack(pady=(15, 4))
entry_format = ctk.CTkEntry(app, width=150)
entry_format.pack()

# Affichage des formats compatibles
ctk.CTkLabel(app, text="Formats disponibles :").pack(pady=(15, 4))
formats_label = ctk.CTkLabel(app, text=f"Image: {image_formats}\nAudio: {audio_formats}\nVidéo: {video_formats}")
formats_label.pack(pady=(4, 10))

ctk.CTkButton(app, text="🚀 Convertir", command=convert, fg_color="#3B82F6").pack(pady=20)

# Démarrage de l'application
app.mainloop()
