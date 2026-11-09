import urllib.request
import urllib.parse

def obter_clima(cidade="Rio de Janeiro"):
    """Consulta o clima atual na internet em tempo real."""
    try:
        cidade_url = urllib.parse.quote(cidade)
        url = f"https://pt.wttr.in/{cidade_url}?format=%t+%C"
        
        # Agora o site sabe que é um programa a pedir, e envia só o texto puro!
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            clima = response.read().decode('utf-8').strip()
            
        return f"Senhor, o clima atual no {cidade} é de {clima}."
        
    except Exception as e:
        print(f"\n[❌ Erro no clima: {e}]\n")
        return "Desculpe, senhor. Não consegui estabelecer ligação com os satélites meteorológicos."