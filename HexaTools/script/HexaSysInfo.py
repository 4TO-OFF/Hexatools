import platform
import psutil
import socket
import time
import requests
import os
import sys

def print_green(text):
    sys.stdout.write(f"\033[92m{text}\033[0m")
    sys.stdout.flush()

def type_effect(text, delay=0.05):
    for char in text:
        print_green(char)
        time.sleep(delay)
    print_green("\n")

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Inconnue"

def get_public_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except:
        return "Non disponible"

def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    total_disk = round(disk_usage.total / (1024 ** 3), 2)
    used_disk = round(disk_usage.used / (1024 ** 3), 2)
    free_disk = round(disk_usage.free / (1024 ** 3), 2)
    return total_disk, used_disk, free_disk

def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    return str(time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)))

def get_network_info():
    net_if_addrs = psutil.net_if_addrs()
    network_info = {}
    for interface, addresses in net_if_addrs.items():
        for addr in addresses:
            if addr.family == socket.AF_INET:
                network_info[interface] = addr.address
    return network_info

def get_process_details():
    process_details = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        process_details.append(f"PID {proc.info['pid']} - {proc.info['name']} - CPU: {proc.info['cpu_percent']}% - Mem: {proc.info['memory_percent']}%")
    return process_details

def get_network_connections():
    connections = psutil.net_connections(kind='inet')
    connection_info = []
    for conn in connections:
        local_address = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr.ip not in ["0.0.0.0", "::"] else f"Any:{conn.laddr.port}"
        remote_address = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None"
        connection_info.append(f"Local Address: {local_address}, Remote Address: {remote_address}, Status: {conn.status}")
    return connection_info

def get_disk_partitions():
    partitions = psutil.disk_partitions()
    partition_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        partition_info.append(f"Partition: {partition.device} - {partition.mountpoint} - Total: {round(usage.total / (1024 ** 3), 2)} Go - Utilisé: {round(usage.used / (1024 ** 3), 2)} Go - Libre: {round(usage.free / (1024 ** 3), 2)} Go")
    return partition_info

def get_bios_version():
    try:
        with os.popen('wmic bios get smbiosbiosversion') as output:
            bios_version = output.read().strip()
        return bios_version if bios_version else "Non disponible"
    except:
        return "Non disponible"

def get_services():
    services = []
    for service in psutil.win_service_iter():
        services.append(f"{service.name()} - {service.status()}")
    return services

# Fonction principale pour simuler le piratage

def fake_hack():
    os.system('cls' if os.name == 'nt' else 'clear')

    type_effect("Connexion au système...")
    time.sleep(1)
    type_effect("Accès autorisé ✅")
    time.sleep(0.5)

    type_effect("\nRécupération des informations système...")
    time.sleep(1)

    type_effect(f"Nom de la machine : {platform.node()}")
    type_effect(f"Système d'exploitation : {platform.system()} {platform.release()}")
    type_effect(f"Processeur : {platform.processor()}")
    type_effect(f"RAM totale : {round(psutil.virtual_memory().total / (1024 ** 3), 2)} Go")
    type_effect(f"Nombre de cœurs CPU : {psutil.cpu_count(logical=True)}")
    
    time.sleep(1)

    # Affichage des partitions de disque
    type_effect("\nAnalyse des partitions de disque...\n")
    partitions = get_disk_partitions()
    for partition in partitions:
        print_green(f"{partition}\n")
    time.sleep(0.5)

    # Affichage de la version du BIOS
    type_effect("\nAnalyse du BIOS...\n")
    type_effect(f"Version du BIOS : {get_bios_version()}")
    
    # Affichage des services actifs
    type_effect("\nAnalyse des services actifs...\n")
    services = get_services()
    for service in services:
        print_green(f"{service}\n")
    time.sleep(0.5)

    type_effect("\nAnalyse des processus en cours...\n")
    time.sleep(0.5)
    process_details = get_process_details()
    for proc in process_details:
        print_green(f"{proc}\n")
    time.sleep(0.5)

    type_effect("\nAnalyse de l'IP...\n")
    type_effect(f"Adresse IP locale : {get_local_ip()}")
    type_effect(f"Adresse IP publique : {get_public_ip()}")

    type_effect("\nAnalyse du disque...\n")
    total_disk, used_disk, free_disk = get_disk_info()
    type_effect(f"Total : {total_disk} Go, Utilisé : {used_disk} Go, Libre : {free_disk} Go")

    type_effect("\nUptime du système : " + get_uptime())

    type_effect("\nAnalyse des connexions réseau...\n")
    connections = get_network_connections()
    print_green("\n".join(connections))
    time.sleep(0.5)

    type_effect("\n - - -\n")
    type_effect("\nToutes tes infos sont là 😈\n")
    input("Appuie sur Entrée pour fermer...")

fake_hack()
