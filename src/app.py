import subprocess
import os
import platform

# Função para verificar se o comando do terminal existe (Linux)
def check_terminal_available_linux(terminal):
    try:
        subprocess.run([terminal, "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# Função para verificar se o comando do terminal existe (Windows)
def check_terminal_available_windows(terminal):
    try:
        subprocess.run([terminal, "/?"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# Função para verificar qual terminal está disponível
def get_available_terminal():
    system = platform.system().lower()
    
    # Para Linux
    if system == 'linux':
        terminals = ["xterm", "gnome-terminal", "konsole", "terminator"]
        for terminal in terminals:
            if check_terminal_available_linux(terminal):
                print(f"{terminal} está disponível.")
                return terminal

    # Para Windows
    elif system == 'windows':
        terminals = ["cmd", "powershell", "wt"]  # "wt" é o Windows Terminal
        for terminal in terminals:
            if check_terminal_available_windows(terminal):
                print(f"{terminal} está disponível.")
                return terminal
    
    print("Nenhum terminal encontrado.")
    return None

# Obter terminal disponível
available_terminal = get_available_terminal()

# Caso um terminal esteja disponível, execute o comando
if available_terminal:
    script_path = "h/src/input_.py"  # Caminho para o seu script
    
    # Exemplo de execução com xterm (Linux)
    if available_terminal == "xterm":
        subprocess.Popen(["xterm", "-hold", "-e", f"python3 {script_path}"])
    # Exemplo de execução com gnome-terminal (Linux)
    elif available_terminal == "gnome-terminal":
        subprocess.Popen(["gnome-terminal", "--", "python3", script_path])
    # Exemplo de execução com PowerShell (Windows)
    elif available_terminal == "powershell":
        subprocess.Popen(["powershell", "-Command", f"python {script_path}"])
    # Exemplo de execução com cmd (Windows)
    elif available_terminal == "cmd":
        subprocess.Popen(["cmd", "/K", f"python {script_path}"])
    # Exemplo de execução com Windows Terminal (Windows)
    elif available_terminal == "wt":
        subprocess.Popen(["wt", "-e", f"python {script_path}"])

else:
    print("Não foi possível abrir o terminal.")