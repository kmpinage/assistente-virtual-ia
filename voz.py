import asyncio
import os
import pygame
import speech_recognition as sr
import edge_tts

# Configurações de voz (Voz da Francisca ou Antonio da Microsoft em PT-BR)
VOICE = "pt-BR-AntonioNeural"
AUDIO_FILE = "resposta.mp3"

async def gerar_audio(texto):
    """Sintetiza texto em fala e salva em arquivo .mp3"""
    communicate = edge_tts.Communicate(texto, VOICE)
    await communicate.save(AUDIO_FILE)

def tocar_audio():
    """Reproduz o arquivo de áudio gerado"""
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)

def falar(texto):
    """Função wrapper para gerar e tocar a voz do JARVIS"""
    print(f"JARVIS: {texto}")
    asyncio.run(gerar_audio(texto))
    tocar_audio()

def ouvir_microfone():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[🎤 Calibrando ruído ambiente...]")
        # 1 segundo inteiro para ele entender exatamente qual é o barulho do quarto
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Devolvemos a inteligência automática para não travar
        recognizer.dynamic_energy_threshold = True
        
        # Mantemos os 2 segundos de pausa. É o suficiente para a palavra "obediente" não ser cortada
        recognizer.pause_threshold = 2.0 
        
        print("[🎤 Pode falar, senhor. (Estou ouvindo até você fazer silêncio...)]")
        
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            
            print("[⌛ Traduzindo áudio para texto...]")
            texto = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você: {texto}")
            return texto.lower()
            
        except sr.UnknownValueError:
            print("[⚠️ O áudio não ficou claro.]")
            return ""
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print(f"[❌ Erro no microfone: {e}]")
            return ""