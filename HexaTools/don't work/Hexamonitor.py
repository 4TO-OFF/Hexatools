import customtkinter as ctk
import GPUtil
import wmi
import threading
import time

# 🌑 Thème sombre
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Fonction pour obtenir les températures
def get_temperatures():
    cpu_temp = None
    gpu_temp = None

    # Essai d'obtenir la température CPU via WMI
    try:
        w = wmi.WMI(namespace="root\\wmi")
        for sensor in w.query("SELECT * FROM MSAcpi_ThermalZoneTemperature"):
            cpu_temp = sensor.CurrentTemperature / 10 - 273.15  # Conversion de la température Kelvin à Celsius
            break
    except Exception as e:
        print(f"Erreur WMI pour le CPU: {e}")

    # Récupération de la température GPU via GPUtil
    try:
        for gpu in GPUtil.getGPUs():
            if gpu.temperature:
                gpu_temp = gpu.temperature
                break
    except Exception as e:
        print(f"Erreur GPUtil pour le GPU: {e}")
    
    return cpu_temp, gpu_temp

# Fonction pour mettre à jour les températures
def update_temps():
    while True:
        cpu_temp, gpu_temp = get_temperatures()
        
        # Mise à jour des valeurs de la température dans l'interface
        temp_label.after(0, lambda: temp_label.configure(text=f"🔥 CPU: {cpu_temp:.2f}°C\n🎮 GPU: {gpu_temp if gpu_temp is not None else 'N/A'}°C"))
        
        time.sleep(1)  # Mise à jour chaque seconde

# Initialisation de l'interface graphique
root = ctk.CTk()
root.title("HexaMonitor - Températures CPU/GPU")
root.geometry("800x400")

# 🖼️ Affichage de la température CPU et GPU
temp_label = ctk.CTkLabel(root, text="Chargement...", font=("Arial", 18))
temp_label.pack(pady=20)

# 🎛️ Lancement de l'update dans un thread séparé
temperature_thread = threading.Thread(target=update_temps, daemon=True)
temperature_thread.start()

# 🌟 Lancer l'application
root.mainloop()
