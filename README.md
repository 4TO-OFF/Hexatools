# 🧰 HexaTools V 0.6.0 - Suite d'outils pratiques

## 📌 Présentation
HexaTools est un projet regroupant plusieurs mini-outils pensés pour faciliter des tâches techniques du quotidien : QR code, analyse de fichiers, réseau, sécurité, et plus encore.  
Certains outils sont finalisés et fonctionnels, d'autres sont encore en cours de développement ou rencontrent des bugs.

---

## ✅ Outils Fonctionnels

| **Nom**       | **Fonction**                                                                 |
|---------------|-------------------------------------------------------------------------------|
| **HexaPass - v1.0**  | Vérifie et complexifie des mots de passe + test brute force 📛               |
| **HexaPort - v1.0**  | Scanner de ports TCP/UDP ⚙️                                                 |
| **HexaQR - v1.0**    | Générateur de QR codes 🔳                                                    |
| **HexaInfo - v1.0**  | Analyse complète de fichiers : métadonnées, permissions, type réel 📂        |
| **HexaNe - v1.0t**   | Monitoring réseau : IP, MAC, ping, vitesse de connexion 🌐                   |
| **HexaCrypt - v1.0** | Crypte les fichier avec un système de mot de passe 🔐                        |

---

## ❌ Outils Non Fonctionnels ou en Pause

| **Nom**         | **Problème actuel**                                                                           |
|-----------------|-----------------------------------------------------------------------------------------------|
| **HexaConvert** | Ne fonctionne pas sans des outils externes compliqués à installer 🔧                          |
| **HexaClean**   | Freeze ou crash pendant l’analyse des fichiers / doublons 💥                                  |
| **HexaFind**    | Trop lent, freeze facilement si beaucoup de fichiers à chercher 🐢                            |
| **HexaMonitor** | Affichage instable, infos système mal rafraîchies 🧯                                           |
| **HexaScan**    | Pas assez précis pour les besoins actuels, nécessite une refonte complète 🔬                  |

---

## 🛠 Installation

### 📎 Pré-requis :
- Python 3.x
- Modules nécessaires :  
  `customtkinter`, `socket`, `qrcode`, `PIL`, etc.

### 🔧 Installation rapide :
```bash
pip install -r requirements.txt
```
ou 

```bash
requis.bat
```

## 📂 Structure du projet

```
HexaTools/
├── Launcher/
├── requis/
├─┬─ script/
| ├── hexapass/
| ├── hexaport/
| ├── hexaqr/
| ├── hexainfo/
| ├── hexanet/
| └── hexashort/
|
├─┬─ don't work/
| └── scripts non fonctionelles/
|
└── README.md
```

---

## 📄 Licence
Projet open-source sous licence **MIT**.

---

## 👤 Créateur
Développé par **4TO_OFF**

- 🔗 [GitHub](https://github.com/4TO-OFF)
- 💙 [Ko-fi](https://ko-fi.com/4to_off)
- 💬 [Discord](https://discord.gg/WpwYCyWsxN)
- 📺 [YouTube](http://www.youtube.com/@4TO_OFF)
