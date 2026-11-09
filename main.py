from voz import ouvir_microfone, falar
from brain import processar_resposta
from comandos_pc import executar_comando_local
from apis import obter_clima

WAKE_WORD = "jarvis"

# A sua cidade padrão (caso você pergunte apenas "Qual o clima?")
CIDADE_PADRAO = "Rio de Janeiro"

def extrair_cidade(comando):
    """Tenta descobrir se o utilizador falou o nome de alguma cidade."""
    if " em " in comando:
        return comando.split(" em ")[-1].strip()
    elif " de " in comando:
        return comando.split(" de ")[-1].strip()
    return CIDADE_PADRAO

if __name__ == "__main__":
    #falar("Sistemas em modo de prontidão. A aguardar chamada, senhor.")
    
    modo_atencao = False
    
    while True:
        comando_usuario = ouvir_microfone()
        
        if not comando_usuario:
            continue
            
        # --- ESTADO 1: STANDBY ---
        if not modo_atencao:
            if WAKE_WORD in comando_usuario:
                pergunta_limpa = comando_usuario.replace(WAKE_WORD, "").strip()
                
                if "desligar" in pergunta_limpa or "encerrar" in pergunta_limpa:
                    falar("A desligar sistemas. Até logo, senhor.")
                    break
                    
                if pergunta_limpa == "":
                    falar("Sim, senhor?")
                    modo_atencao = True
                    continue
                
                # --- INTERCETADORES ---
                resposta_pc = executar_comando_local(pergunta_limpa)
                if resposta_pc:
                    falar(resposta_pc)
                elif "clima" in pergunta_limpa or "tempo" in pergunta_limpa or "temperatura" in pergunta_limpa:
                    cidade_alvo = extrair_cidade(pergunta_limpa)
                    falar(obter_clima(cidade_alvo))
                else:
                    resposta = processar_resposta(pergunta_limpa)
                    falar(resposta)
                    
                modo_atencao = True 
            else:
                print("[Standby - A aguardar Wake Word...]")
        
        # --- ESTADO 2: ACORDADO ---
        else:
            if any(palavra in comando_usuario for palavra in ["obrigado", "dispensado", "descansar", "só isso"]):
                falar("À sua disposição, senhor.")
                modo_atencao = False
                continue
                
            if "desligar" in comando_usuario or "encerrar" in comando_usuario:
                falar("A desligar sistemas. Até logo, senhor.")
                break
                
            # --- INTERCETADORES ---
            resposta_pc = executar_comando_local(comando_usuario)
            if resposta_pc:
                falar(resposta_pc)
            elif "clima" in comando_usuario or "tempo" in comando_usuario or "temperatura" in comando_usuario:
                cidade_alvo = extrair_cidade(comando_usuario)
                falar(obter_clima(cidade_alvo))
            else:
                resposta = processar_resposta(comando_usuario)
                falar(resposta)