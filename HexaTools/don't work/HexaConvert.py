from PIL import Image
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os

# Fonction de conversion d'image
def convert_image(input_path, output_path, output_format):
    try:
        with Image.open(input_path) as img:
            img.convert("RGB").save(output_path, format=output_format)
            print(f"Image convertie et sauvegardée sous {output_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion de l'image : {e}")
        return False
    return True

# Fonction de conversion vidéo en audio
def video_to_audio(input_video, output_audio):
    try:
        video = VideoFileClip(input_video)
        audio = video.audio
        audio.write_audiofile(output_audio)
        print(f"Audio extrait et sauvegardé sous {output_audio}")
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'audio : {e}")
        return False
    return True

# Fonction de conversion audio entre différents formats
def convert_audio(input_audio, output_audio, output_format):
    try:
        audio = AudioSegment.from_file(input_audio)
        audio.export(output_audio, format=output_format)
        print(f"Audio converti et sauvegardé sous {output_audio}")
    except Exception as e:
        print(f"Erreur lors de la conversion de l'audio : {e}")
        return False
    return True

# Fonction principale pour demander à l'utilisateur quel type de conversion il veut faire
def start_conversion():
    while True:
        print("\nQuel type de conversion souhaitez-vous effectuer ?")
        print("1. Image")
        print("2. Vidéo (extraire audio)")
        print("3. Audio")
        print("4. Quitter")

        choice = input("Veuillez entrer votre choix (1/2/3/4) : ")

        if choice == "1":
            input_file = input("Entrez le chemin du fichier image à convertir : ")
            output_file = input("Entrez le chemin de sortie pour l'image : ")
            output_format = input("Entrez le format de sortie (ex. PNG, JPEG) : ")
            convert_image(input_file, output_file, output_format)

        elif choice == "2":
            input_video = input("Entrez le chemin de la vidéo à convertir : ")
            output_audio = input("Entrez le chemin de sortie pour l'audio : ")
            video_to_audio(input_video, output_audio)

        elif choice == "3":
            input_audio = input("Entrez le chemin du fichier audio à convertir : ")
            output_audio = input("Entrez le chemin de sortie pour l'audio : ")
            output_format = input("Entrez le format de sortie (ex. MP3, WAV) : ")
            convert_audio(input_audio, output_audio, output_format)

        elif choice == "4":
            print("Merci d'avoir utilisé HexaTools. À bientôt !")
            break  # Quitter la boucle et le programme

        else:
            print("Choix invalide. Veuillez essayer à nouveau.")

# Lancer la conversion
if __name__ == "__main__":
    start_conversion()
