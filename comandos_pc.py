import webbrowser
import subprocess

def executar_comando_local(comando):
    """Verifica se a frase contém uma ordem para o Windows."""
    
    # Comandos de Navegador
    if "abrir youtube" in comando:
        webbrowser.open("https://www.youtube.com")
        return "A abrir o YouTube, senhor."
        
    elif "abrir google" in comando:
        webbrowser.open("https://www.google.com")
        return "A abrir o Google."
        
    elif "tocar música" in comando or "abrir spotify" in comando:
        # Abre a versão web do Spotify (pode alterar para o .exe se preferir)
        webbrowser.open("https://open.spotify.com")
        return "A iniciar o Spotify."

    # Comandos de Sistema (Windows)
    elif "abrir bloco de notas" in comando:
        subprocess.Popen(["notepad.exe"])
        return "Bloco de notas iniciado."
        
    elif "abrir calculadora" in comando:
        subprocess.Popen(["calc.exe"])
        return "Calculadora no ecrã."
        
    # Retorna None se não encontrou nenhum comando local na frase
    return None