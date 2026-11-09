import asyncio
import os
import edge_tts
import pygame

# Voz neural masculina
VOZ_JARVIS = "pt-BR-AntonioNeural"

# Meio termo ideal: +8% ou +10% (teste alterar entre +5% e +12%)
VELOCIDADE = "+20%"

async def _gerar_audio(texto, caminho_arquivo):
    communicate = edge_tts.Communicate(texto, VOZ_JARVIS, rate=VELOCIDADE)
    await communicate.save(caminho_arquivo)

def falar(texto):
    """Converte texto em voz neural com velocidade calibrada"""
    if not texto:
        return

    print(f"\n🤖 JARVIS: {texto}")
    temp_audio = "temp_resposta.mp3"

    try:
        asyncio.run(_gerar_audio(texto, temp_audio))

        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()

        if os.path.exists(temp_audio):
            os.remove(temp_audio)

    except Exception as e:
        print(f"Erro na síntese de voz: {e}")

if __name__ == "__main__":
    falar("Sistemas totalmente online, senhor. Como posso ajudar você hoje?")