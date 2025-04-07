import socket
import threading
import customtkinter as ctk
from datetime import datetime

# 🎨 Thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 🔍 Fonction de scan
def scan_ports():
    ip = entry_ip.get()
    try:
        port_start = int(entry_start.get())
        port_end = int(entry_end.get())
    except ValueError:
        result_textbox.insert("end", "❌ Plage de ports invalide.\n")
        return

    is_udp = udp_var.get() == "UDP"
    total_ports = port_end - port_start + 1
    progress_bar.set(0)
    result_textbox.delete("1.0", "end")
    result_textbox.insert("end", f"📡 Scan {('UDP' if is_udp else 'TCP')} de {ip} de {port_start} à {port_end}...\n")
    start_time = datetime.now()

    # Désactiver les inputs
    scan_button.configure(state="disabled")
    entry_ip.configure(state="disabled")
    entry_start.configure(state="disabled")
    entry_end.configure(state="disabled")
    mode_switch.configure(state="disabled")

    def scanner():
        for idx, port in enumerate(range(port_start, port_end + 1)):
            try:
                if is_udp:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(0.5)
                    sock.sendto(b"", (ip, port))
                    try:
                        data, _ = sock.recvfrom(1024)
                        result_textbox.insert("end", f"🟧 Port UDP {port} : réponse reçue\n")
                    except socket.timeout:
                        result_textbox.insert("end", f"🟨 Port UDP {port} : pas de réponse (peut être ouvert)\n")
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "inconnu"
                        result_textbox.insert("end", f"✅ Port TCP {port} ouvert ({service})\n")
                sock.close()
            except:
                continue
            progress_bar.set((idx + 1) / total_ports)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        result_textbox.insert("end", f"\n🕒 Terminé en {duration:.2f} secondes.\n")

        # Réactiver les inputs
        scan_button.configure(state="normal")
        entry_ip.configure(state="normal")
        entry_start.configure(state="normal")
        entry_end.configure(state="normal")
        mode_switch.configure(state="normal")

    threading.Thread(target=scanner).start()

# 💻 Interface
app = ctk.CTk()
app.title("HexaPort - Scanner TCP/UDP")
app.geometry("500x600")

ctk.CTkLabel(app, text="🌐 IP à scanner :").pack(pady=5)
entry_ip = ctk.CTkEntry(app, width=300)
entry_ip.insert(0, "127.0.0.1")
entry_ip.pack(pady=5)

ctk.CTkLabel(app, text="🔢 Port de début :").pack(pady=5)
entry_start = ctk.CTkEntry(app, width=100)
entry_start.insert(0, "1")
entry_start.pack(pady=5)

ctk.CTkLabel(app, text="🔢 Port de fin :").pack(pady=5)
entry_end = ctk.CTkEntry(app, width=100)
entry_end.insert(0, "100")
entry_end.pack(pady=5)

# 🌐 Mode TCP / UDP
ctk.CTkLabel(app, text="📶 Protocole :").pack(pady=5)
udp_var = ctk.StringVar(value="TCP")
mode_switch = ctk.CTkSegmentedButton(app, values=["TCP", "UDP"], variable=udp_var)
mode_switch.pack(pady=5)

# 🚀 Bouton scan
scan_button = ctk.CTkButton(app, text="🚀 Lancer le scan", command=scan_ports)
scan_button.pack(pady=15)

# 🔄 Barre de progression
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)

# 📜 Résultats
result_textbox = ctk.CTkTextbox(app, width=460, height=300)
result_textbox.pack(pady=10)

app.mainloop()
