import customtkinter as ctk
import tkinter as tk
import psutil
import socket
import platform
import threading
import time
import subprocess
import scapy.all as scapy

# 🎨 Thème sombre & bleu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 🖼️ Fenêtre principale
app = ctk.CTk()
app.title("HexaNetwork - Analyse Réseau")
app.geometry("600x600")

# 📡 Infos de base
def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    interfaces = psutil.net_if_addrs()
    mac_address = "Inconnu"
    for interface in interfaces.values():
        for snic in interface:
            if snic.family == psutil.AF_LINK:
                mac_address = snic.address
                break

    label_ip.configure(text=f"🌐 IP : {ip_address}")
    label_mac.configure(text=f"🔗 MAC : {mac_address}")
    label_wifi.configure(text=f"📶 Réseau : {hostname}")

# 🔁 Fonction ping
def ping():
    target = entry_target.get()
    while var_ping.get():
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            output = subprocess.check_output(["ping", param, "1", target], stderr=subprocess.DEVNULL)
            ping_result = output.decode(errors="ignore")
            # 🔍 Extraction du temps de ping
            if "ms" in ping_result:
                time_ms = ping_result.split("time=")[-1].split("ms")[0].strip()
                label_ping.configure(text=f"📡 Ping : {time_ms} ms")
            else:
                label_ping.configure(text="📡 Ping : timeout")
        except:
            label_ping.configure(text="📡 Ping : erreur")
        time.sleep(1)

def toggle_ping():
    if var_ping.get():
        threading.Thread(target=ping, daemon=True).start()
    else:
        label_ping.configure(text="📡 Ping : arrêté")

# 🌐 Scan réseau local (détection des appareils)
def scan_ip_range(ip_range):
    """Scan un réseau local pour détecter les appareils actifs"""
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        device_info = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc
        }
        devices.append(device_info)
    
    return devices

def display_devices(devices):
    """Affiche les appareils trouvés sur le réseau"""
    label_devices.configure(text="Appareils détectés sur le réseau :")
    for device in devices:
        label_devices_info.configure(text=f"{device['ip']} - {device['mac']}")

# 🎛️ Widgets
frame_main = ctk.CTkFrame(app)
frame_main.pack(pady=20, padx=20, fill="both", expand=True)

entry_target = ctk.CTkEntry(frame_main, placeholder_text="Adresse à pinger (ex: 8.8.8.8)", width=300)
entry_target.pack(pady=10)
entry_target.insert(0, "8.8.8.8")

btn_toggle_ping = ctk.CTkSwitch(frame_main, text="Activer le ping", variable=ctk.BooleanVar(value=False), command=toggle_ping)
btn_toggle_ping.pack(pady=10)
var_ping = btn_toggle_ping.cget("variable")

label_ping = ctk.CTkLabel(frame_main, text="📡 Ping : ...")
label_ping.pack(pady=10)

label_ip = ctk.CTkLabel(frame_main, text="🌐 IP : ...")
label_ip.pack(pady=5)

label_mac = ctk.CTkLabel(frame_main, text="🔗 MAC : ...")
label_mac.pack(pady=5)

label_wifi = ctk.CTkLabel(frame_main, text="📶 Réseau : ...")
label_wifi.pack(pady=5)

# Afficher les appareils détectés sur le réseau
label_devices = ctk.CTkLabel(frame_main, text="Appareils détectés : ...")
label_devices.pack(pady=5)

label_devices_info = ctk.CTkLabel(frame_main, text="...")
label_devices_info.pack(pady=5)

# 📦 Chargement des infos réseau au démarrage
get_network_info()

# 🎯 Bouton pour scanner les appareils du réseau
btn_scan_devices = ctk.CTkButton(frame_main, text="Scanner le réseau", command=lambda: display_devices(scan_ip_range("192.168.1.1/24")))
btn_scan_devices.pack(pady=10)

# 🚀 Lancement de l'app
app.mainloop()
