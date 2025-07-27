import ctypes
import time
import os
import subprocess
import getpass


def _verificar_admin():
    """Verifica se o script está sendo executado como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def _configurar_energia_remoto():
    """Configura as opções de energia em um computador remoto via PowerShell Remoting"""
    
    print("\n=== Configurador de Energia Remoto ===")
    
    # Coletar credenciais
    computador = input("\nNome do computador ou IP: ")
    usuario = input("Usuário (formato DOMÍNIO\\usuário): ")
    senha = getpass.getpass("Senha: ")
    
    # Script PowerShell que será executado remotamente
    ps_script = f"""
    $ErrorActionPreference = "Stop"
    
    try {{
        # 1. Ativar plano equilibrado
        powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
        
        # 2. Configurar para nunca desligar disco, tela ou suspender
        $configs = @(
            @{{Grupo='0012ee47-9041-4b5d-9b77-535fba8b1442'; Subgrupo='6738e2c4-e8a5-4a42-b16a-e040e769756e'}}, # Disco
            @{{Grupo='7516b95f-f776-4464-8c53-06167f40cc99'; Subgrupo='3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e'}}, # Vídeo
            @{{Grupo='238c9fa8-0aad-41ed-83f4-97be242c8f20'; Subgrupo='29f6c1db-86da-48c5-9fdb-f2b67b1f44da'}}  # Suspensão
        )
        
        foreach ($cfg in $configs) {{
            powercfg /setacvalueindex 381b4222-f694-41f0-9685-ff5bb260df2e $cfg.Grupo $cfg.Subgrupo 0
            powercfg /setdcvalueindex 381b4222-f694-41f0-9685-ff5bb260df2e $cfg.Grupo $cfg.Subgrupo 0
        }}
        
        # 3. Desativar hibernação
        powercfg /hibernate off
        
        return "Configurações aplicadas com sucesso em $env:COMPUTERNAME"
    }}
    catch {{
        return "ERRO: $_"
    }}
    """
    
    # Comando para executar via PowerShell Remoting
    comando = [
        "powershell",
        "-Command",
        f"$secpass = ConvertTo-SecureString '{senha}' -AsPlainText -Force;",
        f"$cred = New-Object System.Management.Automation.PSCredential('{usuario}', $secpass);",
        f"Invoke-Command -ComputerName {computador} -Credential $cred -ScriptBlock {{{ps_script}}}"
    ]
    
    print(f"\n Aplicando configurações em {computador}...")
    
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("\n" + resultado.stdout)
        if "ERRO:" in resultado.stdout:
            print("\n Falha na configuração remota.")
        else:
            print("\n Configuração aplicada com sucesso!")
            
    except subprocess.CalledProcessError as e:
        print(f"\n Erro ao conectar: {e.stderr}")

def menu_principal():
    if not _verificar_admin():
        print(" Este script precisa ser executado como Administrador.")
        return
    
    os.system("cls")
    print("\n" + "="*50)
    print("=== Configurador de Plano de Energia REMOTO - v1.0.0 ===")
    print("="*50)
    print("\n Este script irá configurar todas as opções como NUNCA por padrão e desligar o disco rídigo.")
    print("Aguarde enquanto as configurações são aplicadas... \n")
    time.sleep(2)
    
    if _configurar_energia_remoto():
        print("\n Pronto! Seu computador não entrará em modo de economia de energia.")
    else:
        print("\n Algo deu errado. Verifique as permissões.")
    
    print("\n Encerrando em 3 segundos...")
    time.sleep(3)

if __name__ == "__main__":
    menu_principal()


""" Version: 1.0.0
Creator: João Malfatti 

Objetivo: Deixar as opções como NUNCA no Plano de Energia com acesso REMOTO."""