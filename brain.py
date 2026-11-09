import concurrent.futures
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

CAMINHO_PASTA = os.path.dirname(__file__)
caminho_env = os.path.join(CAMINHO_PASTA, ".env")
load_dotenv(dotenv_path=caminho_env)

client = genai.Client()
CAMINHO_MEMORIA = os.path.join(CAMINHO_PASTA, "memoria.json")

# NOVA VARIÁVEL: Guarda as últimas interações para dar contexto (Memória Curta)
historico_conversa = []

def carregar_memoria():
    if os.path.exists(CAMINHO_MEMORIA):
        with open(CAMINHO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _executar_requisicao_gemini(texto_usuario, system_instruction):
    global historico_conversa
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7,
        max_output_tokens=250,
        tools=[{"google_search": {}}] # Acesso total à internet destrancado aqui!
    )
    
    # MÁGICA DA MEMÓRIA: Injetamos o histórico recente invisivelmente na sua pergunta
    prompt_com_contexto = "Histórico recente da nossa conversa:\n"
    for linha in historico_conversa:
        prompt_com_contexto += f"{linha}\n"
    prompt_com_contexto += f"\nComando atual do usuário: {texto_usuario}"
    
    modelos_salvacao = [
        "gemini-flash-lite-latest", # O mais rápido assume a liderança
        "gemini-2.5-flash",         # O mais pesado fica como reserva
        "gemini-3.5-flash-lite" 
    ]
    
    for modelo in modelos_salvacao:
        for tentativa in range(1, 3):
            try:
                response = client.models.generate_content(
                    model=modelo,
                    contents=prompt_com_contexto,
                    config=config
                )
                resposta_texto = response.text.strip()
                
                # Se deu certo, salva a sua pergunta e a resposta dele no histórico!
                historico_conversa.append(f"Usuário: {texto_usuario}")
                historico_conversa.append(f"JARVIS: {resposta_texto}")
                
                # Mantém apenas as últimas 6 mensagens (3 trocas) para não pesar na memória
                if len(historico_conversa) > 6:
                    historico_conversa = historico_conversa[-6:]
                    
                return resposta_texto
                
            except Exception as e:
                erro_str = str(e)
                if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                    break 
                elif "503" in erro_str or "UNAVAILABLE" in erro_str:
                    time.sleep(1)
                else:
                    break 
                    
    raise Exception("Todos os modelos de resgate falharam.")

def processar_resposta(texto_usuario):
    if not texto_usuario:
        return ""

    print("[🧠 Processando resposta...]")
    memoria = carregar_memoria()
    
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    system_instruction = f"""
    Você é o JARVIS, um assistente virtual leal, altamente inteligente e eficiente.
    
    INFORMAÇÕES DE TEMPO REAL:
    - Data e hora exatas de agora: {agora}
    
    Conhecimento sobre o seu usuário e ambiente:
    {json.dumps(memoria, ensure_ascii=False, indent=2)}

    Regras de resposta:
    1. Responda de forma DIRETA e EXTREMAMENTE CONCISA (máximo de 1 a 2 frases curtas). Vá direto ao ponto sem introduções.
    2. Não use caracteres especiais ou marcações Markdown (*, #, etc).
    3. Trate o usuário por "Senhor".
    4. Eu vou te enviar o histórico recente. Use-o para entender de quem/do que eu estou falando!
    """

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_executar_requisicao_gemini, texto_usuario, system_instruction)
        try:
            return future.result(timeout=15.0)
        except concurrent.futures.TimeoutError:
            return "Desculpe, senhor. A rede demorou muito para responder."
        except Exception as e:
            return "Desculpe, senhor. Os servidores estão passando por instabilidade no momento."

if __name__ == "__main__":
    # Teste 1: Pergunta isolada
    resposta_1 = processar_resposta("Qual é a capital da França?")
    print(f"JARVIS: {resposta_1}")
    
    # Teste 2: Pergunta dependente do contexto (Memória)
    resposta_2 = processar_resposta("Qual é a população dela?")
    print(f"JARVIS: {resposta_2}")