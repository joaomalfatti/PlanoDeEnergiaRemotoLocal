import ctypes
import time
import os
import subprocess

# Constantes dos GUID's
PLANO_EQUILIBRADO = '381b4222-f694-41f0-9685-ff5bb260df2e'

CONFIGURACOES_ENERGIA = [
    # Disco rígido
    ('0012ee47-9041-4b5d-9b77-535fba8b1442', '6738e2c4-e8a5-4a42-b16a-e040e769756e', '0'),
    # Vídeo
    ('7516b95f-f776-4464-8c53-06167f40cc99', '3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e', '0'),
    # Suspensão
    ('238c9fa8-0aad-41ed-83f4-97be242c8f20', '29f6c1db-86da-48c5-9fdb-f2b67b1f44da', '0')
]


def _verificar_admin():
    """Verifica se o script está sendo executado como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _aplicar_configuracoes_energia():
    """Configura as opções de energia padrão."""
    try:
        print("\n Aplicando configurações de energia...")

        # Ativar plano equilibrado
        subprocess.run(['powercfg', '/setactive', PLANO_EQUILIBRADO], check=True)

        # Aplicar configurações AC/DC
        for grupo, subgrupo, valor in CONFIGURACOES_ENERGIA:
            for modo in ['setacvalueindex', 'setdcvalueindex']:
                comando = ['powercfg', f'/{modo}', PLANO_EQUILIBRADO, grupo, subgrupo, valor]
                subprocess.run(comando, check=True)

        # Desativar hibernação
        subprocess.run(['powercfg', '/hibernate', 'off'], check=True)

        print("\n Configurações aplicadas com sucesso!")
        print(" Disco rígido: Nunca desligar")
        print(" Vídeo: Nunca desligar")
        print(" Suspensão: Nunca")
        print(" Hibernação: Desativada")

        return True

    except subprocess.CalledProcessError as erro:
        print(f"\n Erro ao aplicar configurações: {erro}")
        return False

def menu_principal():
    if not _verificar_admin():
        print(" Este script precisa ser executado como Administrador.")
        return
    
    os.system("cls")
    print("\n" + "="*50)
    print("=== Configurador de Plano de Energia - v1.0.0 ===")
    print("="*50)
    print("\n Este script irá configurar todas as opções como NUNCA por padrão e desligar o disco rídigo.")
    print("Aguarde enquanto as configurações são aplicadas... \n")
    time.sleep(2)
    
    if _aplicar_configuracoes_energia():
        print("\n Pronto! Seu computador não entrará em modo de economia de energia.")
    else:
        print("\n Algo deu errado. Verifique as permissões.")
    
    print("\n Encerrando em 3 segundos...")
    time.sleep(3)

if __name__ == "__main__":
    menu_principal()


""" Version: 1.0.0
Creator: João Malfatti """