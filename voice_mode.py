import os
from pathlib import Path
from dotenv import load_dotenv
from nova.assistant import NovaAssistant
from nova.voice import listen_once
load_dotenv(); base=Path(__file__).resolve().parent
nova=NovaAssistant(base/'workspace')
nova.speak('Olá, sou a NOVA, criada por John Sky da JOHN SKY DESIGN. Estou pronta.')
while True:
    cmd=listen_once(os.getenv('NOVA_LANGUAGE','pt-PT'))
    if cmd=='[SEM_INTERNET]': nova.speak('Estou sem Internet. Os comandos locais continuam disponíveis.'); continue
    if not cmd: continue
    print('Tu:',cmd)
    if any(x in cmd.lower() for x in ['desligar nova','terminar assistente','até logo']):
        nova.speak('Até já.'); break
    nova.speak(nova.handle(cmd))
