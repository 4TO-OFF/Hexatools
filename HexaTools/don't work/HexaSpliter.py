import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📁 HexaSplitter")
app.geometry("500x400")

mode = ctk.StringVar(value="split")

def split_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        percent = int(entry_percent.get())
        if not 1 <= percent < 100:
            raise ValueError
    except:
        messagebox.showerror("Erreur", "Pourcentage invalide (1-99).")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    part_size = len(data) * percent // 100
    total_parts = (len(data) + part_size - 1) // part_size
    base_name = os.path.basename(file_path)
    output_dir = os.path.dirname(file_path)

    for i in range(total_parts):
        part_data = data[i * part_size:(i + 1) * part_size]
        with open(os.path.join(output_dir, f"{base_name}.part{i}"), "wb") as part_file:
            part_file.write(part_data)

    messagebox.showinfo("✅ Fait", f"{total_parts} morceaux créés.")

def join_files():
    files = filedialog.askopenfilenames(title="Sélectionne les morceaux à regrouper")
    if not files:
        return

    files = sorted(files)
    output_path = filedialog.asksaveasfilename(defaultextension=".joined")

    with open(output_path, "wb") as outfile:
        for file in files:
            with open(file, "rb") as part:
                outfile.write(part.read())

    messagebox.showinfo("✅ Fait", f"Fichier reconstruit : {output_path}")

def handle_action():
    if mode.get() == "split":
        split_file()
    else:
        join_files()

# === UI ===
label_mode = ctk.CTkLabel(app, text="🧰 Choisis une action :")
label_mode.pack(pady=10)

combo_mode = ctk.CTkOptionMenu(app, values=["split", "join"], variable=mode)
combo_mode.pack()

entry_percent = ctk.CTkEntry(app, placeholder_text="Taille par morceau (%)")
entry_percent.pack(pady=20)

btn_execute = ctk.CTkButton(app, text="🚀 Exécuter", command=handle_action)
btn_execute.pack(pady=10)

app.mainloop()
