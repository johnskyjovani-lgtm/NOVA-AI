import os, datetime, webbrowser, subprocess, platform
from pathlib import Path
from groq import Groq

SYSTEM = '''És a NOVA, assistente do projecto JOHN SKY DESIGN, criada por John Sky em Luanda, Angola. Responde em português claro, preferencialmente português de Angola. Ajudas em informática: Python, HTML, CSS, JavaScript, SQL, redes, hardware, Windows, Office e tarefas do dia a dia. Nunca afirmes que executaste algo quando apenas deste instruções. Nunca peças nem reveles palavras-passe, tokens ou chaves. Se não tiveres acesso a uma função do computador, explica a limitação.'''

class NovaAssistant:
    def __init__(self, workspace):
        self.workspace = Path(workspace).resolve(); self.workspace.mkdir(parents=True, exist_ok=True)
        key = os.getenv('GROQ_API_KEY', '').strip()
        self.client = Groq(api_key=key) if key and key != 'COLOCA_A_TUA_NOVA_CHAVE_AQUI' else None
        self.engine = None; self.voice_ready = False
        try:
            import pyttsx3
            self.engine = pyttsx3.init(); self.engine.setProperty('rate', 170)
            for v in self.engine.getProperty('voices'):
                if any(s in (v.name + v.id).lower() for s in ['portuguese','portugal','brazil','pt-']):
                    self.engine.setProperty('voice', v.id); break
            self.voice_ready = True
        except Exception: pass

    def speak(self, text):
        print('NOVA:', text)
        if self.engine:
            try: self.engine.say(text); self.engine.runAndWait()
            except Exception as e: print('Erro de voz:', e)

    def safe_path(self, name):
        p = (self.workspace / name).resolve()
        if p != self.workspace and self.workspace not in p.parents:
            raise ValueError('Por segurança, só posso criar ficheiros dentro da pasta workspace.')
        return p

    def local_command(self, prompt):
        p = prompt.lower().strip()
        if any(x in p for x in ['que horas são','diz as horas','hora atual']):
            return 'Agora são ' + datetime.datetime.now().strftime('%H:%M') + '.'
        if 'abre o google' in p or 'abrir google' in p:
            webbrowser.open('https://www.google.com'); return 'Abri o Google.'
        if 'abre o youtube' in p or 'abrir youtube' in p:
            webbrowser.open('https://www.youtube.com'); return 'Abri o YouTube.'
        if 'abre o whatsapp' in p:
            webbrowser.open('https://web.whatsapp.com'); return 'Abri o WhatsApp Web. Confirma sempre o destinatário antes de enviar mensagens.'
        if 'abre o bloco de notas' in p or 'abrir bloco de notas' in p:
            if platform.system() == 'Windows': subprocess.Popen(['notepad.exe']); return 'Abri o Bloco de Notas.'
            return 'Este comando está configurado para Windows.'
        if p.startswith('cria nota ') or p.startswith('criar nota '):
            content = prompt.split(' ', 2)[-1].strip()
            path = self.safe_path('nota_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt')
            path.write_text(content, encoding='utf-8'); return 'Criei a nota ' + path.name + ' na pasta workspace.'
        if 'lista os ficheiros' in p or 'listar ficheiros' in p:
            names = [x.name for x in self.workspace.iterdir()]
            return 'Ficheiros: ' + (', '.join(names) if names else 'a pasta está vazia.')
        if 'estado do computador' in p or 'informações do sistema' in p:
            return f'Sistema {platform.system()} {platform.release()}, arquitectura {platform.machine()}, Python {platform.python_version()}.'
        return None

    def handle(self, prompt):
        local = self.local_command(prompt)
        if local is not None: return local
        if not self.client:
            return 'A inteligência Groq não está configurada. Os comandos locais continuam disponíveis. Coloca a tua nova chave no ficheiro .env.'
        try:
            r = self.client.chat.completions.create(model=os.getenv('GROQ_MODEL','openai/gpt-oss-120b'),
                messages=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}], temperature=0.5, max_tokens=1200)
            return r.choices[0].message.content.strip()
        except Exception as e:
            print('Groq:', repr(e)); return 'Não consegui contactar a Groq. Verifica Internet, chave e modelo.'
