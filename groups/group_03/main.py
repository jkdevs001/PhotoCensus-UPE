import os
import sys

GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import *


def ask_folder():
    """
    Ask for the folder name until the user enters a valid one
    """
    show_folders()
    print()

    folder = input("Enter the name of the desired folder: ").strip().lower()
    while not folder_exists(folder):
        print("❌ Folder not found! Check the name you entered and try again.\n")
        show_folders()
        folder = input("Enter the name of the desired folder: ").strip().lower()

    return folder


def ask_photo_number(folder):
    """
    Ask for the photo number and ensure it is between 1 and the total number of photos in the folder.
    """
    total = total_photos(folder)
    num  = int(input(f"Enter the photo number (1 to {total}): "))

    while num < 1 or num > total:
        print(f"Number out of range! Choose a value between 1 and {total}.")

        num  = int(input(f"Enter the photo number (1 to {total}): "))

    return num

def main():
    min_confidence_level = 0.5

    while True:
        print("\n" + "=" * 40)
        print(f"{"PHOTOCENSUS - MENU":^40} Grupo 03")
        print("=" * 40)
        print(f"Current minimun confidence: {min_confidence_level:.2f}")
        print("-" * 40)
        # Configurar confiança mínima
        print("[ 1 ] - Change minimum confidence")
        # Analisar foto
        print("[ 2 ] - Analyze a photo")
        # Contar uma classe na foto
        print("[ 3 ] - Count class in a photo")
        # Relatório da pasta
        print("[ 4 ] - Folder report")
        # Foto mais cheia e mais vazia
        print("[ 5 ] - Most and least populated photo")
        # Procurar uma classe na pasta
        print("[ 6 ] - Search class in folder")
        # Gráfico de barras em texto
        print("[ 7 ] - Bar char (text)")
        # Encerrar Programa
        print("[ 0 ] - Exit")
        print("=" * 40)

        option = input("Choose an option: ").strip()

        if option == "1":
            # Configurar a confiança mínima (validada entre 0 e 1)
            new_conf = float(input("Enter new confidence (0.0 to 1.0): ").strip())

            while new_conf < 0.0 or new_conf > 1.0:
                print("❌ Invalid confidence! Value must be between 0.0 and 1.0")
                new_conf = float(input("Enter new confidence (0.0 to 1.0): ").strip())

            min_confidence_level = new_conf
            print(f"✅ Minimum confidence update to {min_confidence_level:.2f}")


        elif option == "2":

            folder = ask_folder()
            num = ask_photo_number(folder)
            photo = photo_name(folder, num)

            total_objs = count_objects(photo, min_confidence_level)
            main_obj = main_object(photo)
            highest_conf = max_confidence(photo)

            print(f"\n--- Photo Analysis ---")
            print(f"Path: {photo}")
            print(f"Total objects: {total_objs}")
            if main_obj:
                print(f"Main object: {main_obj}")
            print(f"Highest confidence: {highest_conf * 100:.1f}%")

        elif option == "0":
            print("Exiting system. Goodbye!")
            break
        
        else:
            print("❌ Invalid option! Please try again.")

if __name__ == "__main__":
    main()
    print("=" * 50)


# --- Menu Principal ---

def menu():
    caminho_atual = None
    detecoes_atuais = []

    while True:
        print("\n" + "#" * 35)
        print("      PHOTOCENSUS - GRUPO 03")
        print("#" * 35)
        print("1. Processar nova imagem")
        print("2. Ver relatório e gráfico de barras")
        print("3. Limpar dados em memória")
        print("0. Sair")
        print("#" * 35)

        opcao = input("Selecione uma opção: ").strip()

        if opcao == "1":
            caminho, detecoes = processar_imagem()
            if caminho is not None:
                caminho_atual = caminho
                detecoes_atuais = detecoes
        elif opcao == "2":
            exibir_relatorio(caminho_atual, detecoes_atuais)
        elif opcao == "3":
            caminho_atual = None
            detecoes_atuais = []
            print("Memória limpa com sucesso.")
        elif opcao == "0":
            print("\nA encerrar o PhotoCensus. Até breve!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu() 