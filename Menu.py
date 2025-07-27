import os
import time

from Modules import PlanoDeEnergiaLocal
from Modules import PlanoDeEnergiaRemoto

def mostrar_menu():
    logo = r"""
    ╔════════════════════════════╗
    ║    Gerenciador de Energia  ║
    ║       Local ou Remoto      ║
    ╚════════════════════════════╝
        
        Creator by João Malfatti
    """

    print(logo)
    print("=" * 50)
    print("Menu do Gerenciador de Energia".center(50))
    print("=" * 50)
    print(" 1. Plano de Energia Local")
    print(" 2. Plano de Energia Remoto")
    print(" 0. Sair")
    print("=" * 50)

def main():
    while True:
        os.system("cls")
        mostrar_menu()

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            PlanoDeEnergiaLocal.menu_principal()

        elif opcao == "2":
            PlanoDeEnergiaRemoto.menu_principal()

        elif opcao == "0":
            print("Saindo do programa...")
            time.sleep(3)

        else:
            print("Opção inválida. Por favor, tente novamente.")
        
        input("\n Pressione Enter para Continuar...")
            

if __name__ == "__main__":
    main()

