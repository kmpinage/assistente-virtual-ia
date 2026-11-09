import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    client = genai.Client()
    print("Conectado! Enviando pergunta para o gemini-flash-latest...")
    
    inicio = time.time()
    
    # Fazendo a requisição simples, sem limites de tempo artificiais
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Responda rápido: qual é a capital do Brasil?"
    )
    
    fim = time.time()
    tempo_decorrido = fim - inicio
    
    print(f"\n✅ SUCESSO! Tempo de resposta: {tempo_decorrido:.2f} segundos.")
    print(f"JARVIS: {response.text.strip()}")
    
except Exception as e:
    print(f"\n❌ ERRO DETALHADO: {e}")