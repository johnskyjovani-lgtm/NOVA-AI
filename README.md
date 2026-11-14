# NOVA AI — JOHN SKY DESIGN

Assistente inicial para Windows: painel web local, chat Groq, síntese de voz, reconhecimento de voz online e comandos locais limitados.

## Instalação (Windows 10/11)
1. Instala Python 3.10+.
2. Revoga a chave Groq que foi exposta na conversa e cria outra em https://console.groq.com/keys.
3. Copia `.env.example` para `.env` e coloca a nova chave em `GROQ_API_KEY`.
4. Executa `run_nova.bat`; o painel abre em http://127.0.0.1:5055.
5. Para modo de voz contínuo, executa `python voice_mode.py` após instalar as dependências.

Se PyAudio falhar na instalação, instala uma versão compatível com o teu Python. O painel web pode ser usado sem microfone Python.

## Exemplos de comandos locais
"Que horas são?"; "Abre o Google"; "Abre o YouTube"; "Abre o WhatsApp"; "Abre o Bloco de Notas"; "Cria nota comprar cabo de rede"; "Lista os ficheiros"; "Estado do computador"; "Desligar NOVA".

Ficheiros criados ficam dentro de `workspace`. A versão inicial não executa comandos arbitrários de terminal, não apaga ficheiros, não instala programas e não envia mensagens automaticamente. Estas protecções evitam que uma interpretação errada ou prompt malicioso danifique o PC.

## Internet, dados móveis e offline
Qualquer ligação IP funciona: Wi-Fi, Ethernet ou hotspot/dados móveis partilhados pelo telefone. Groq e reconhecimento Google exigem Internet. A voz sintetizada e comandos locais básicos podem funcionar offline. Reconhecimento offline com Vosk exige instalar o pacote e descarregar um modelo de português; não está activado nesta versão.

## WhatsApp
O atalho abre WhatsApp Web. Para envio/recepção automatizados, usa a WhatsApp Business Platform / Cloud API oficial, com conta, número, tokens e consentimento. Nunca coloques tokens no JavaScript nem publiques `.env`.

## Tecnologias
Python, HTML5, CSS3, JavaScript, SQLite/SQL, Flask, Groq API, SpeechRecognition e pyttsx3.

Isto é uma base funcional e extensível, não um agente universal com controlo irrestrito do PC. Novas ferramentas devem ser explícitas, testadas e exigir confirmação para acções sensíveis.

## Interface NOVA AI Lab e instalação como APP
- O logótipo fornecido JOHN SKY DESIGN está em `nova/static/assets/`.
- A interface inclui painel de laboratório, áreas de Assistência Técnica, Programação, Redes e Windows.
- A voz automática pode ser ligada/desligada no painel. Cada resposta também tem o botão “Ouvir resposta”; a leitura usa a voz do navegador.
- O microfone dita para a caixa de texto; o utilizador confirma o envio no botão Enviar.
- O projeto inclui `manifest.json` e `service-worker.js`. Para instalar no Android/PC através da rede, publique o site em HTTPS. Em desenvolvimento, `localhost` também é aceite.
- O service worker guarda apenas a interface e os recursos visuais. A conversa com Groq continua a exigir Internet; a API não é guardada em cache.
- Para Android: abra o endereço HTTPS no Chrome, menu ⋮ e “Instalar app” ou “Adicionar ao ecrã inicial”.
- Para Windows: abra o endereço HTTPS no Chrome/Edge e use o ícone de instalação na barra de endereço ou o botão “Instalar APP”.
- A versão local `http://127.0.0.1:5055` serve para testar no próprio PC. Para o telemóvel, o projeto precisa de alojamento HTTPS acessível pela Internet ou configuração segura na rede local.

Nota: a leitura por voz e o ditado dependem das capacidades e permissões do navegador. O ditado do Chrome/Edge pode exigir Internet.
