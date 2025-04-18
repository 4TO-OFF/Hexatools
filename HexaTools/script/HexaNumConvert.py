import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🧮 Convertisseur Base")
app.geometry("500x400")

# 🔽 Label d'entrée
label_input = ctk.CTkLabel(app, text="Nombre à convertir :", font=("Arial", 16))
label_input.pack(pady=10)

entry = ctk.CTkEntry(app, width=300)
entry.pack()

# 🧭 Choix du type d'entrée
base_var = ctk.StringVar(value="Décimal")

selector = ctk.CTkOptionMenu(app, values=["Binaire", "Décimal", "Hexadécimal"], variable=base_var)
selector.pack(pady=10)

# 📤 Résultats
result_bin = ctk.CTkLabel(app, text="Binaire : ", font=("Arial", 14))
result_bin.pack(pady=5)

result_dec = ctk.CTkLabel(app, text="Décimal : ", font=("Arial", 14))
result_dec.pack(pady=5)

result_hex = ctk.CTkLabel(app, text="Hexadécimal : ", font=("Arial", 14))
result_hex.pack(pady=5)

def convert():
    val = entry.get().strip()
    base = base_var.get()

    try:
        if base == "Décimal":
            number = int(val)
        elif base == "Binaire":
            number = int(val, 2)
        elif base == "Hexadécimal":
            number = int(val, 16)
        else:
            raise ValueError

        result_bin.configure(text=f"Binaire : {bin(number)[2:]}")
        result_dec.configure(text=f"Décimal : {number}")
        result_hex.configure(text=f"Hexadécimal : {hex(number)[2:].upper()}")
    except:
        result_bin.configure(text="Binaire : ⚠️ Erreur")
        result_dec.configure(text="Décimal : ⚠️ Erreur")
        result_hex.configure(text="Hexadécimal : ⚠️ Erreur")

# 🎯 Bouton
btn = ctk.CTkButton(app, text="Convertir 🔁", command=convert)
btn.pack(pady=20)

# 👟 Start
app.mainloop()
