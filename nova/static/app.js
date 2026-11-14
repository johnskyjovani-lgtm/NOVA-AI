const form=document.querySelector('#chatform');
const input=document.querySelector('#prompt');
const messages=document.querySelector('#messages');
const autoVoice=document.querySelector('#autoVoice');
const voiceState=document.querySelector('#voiceState');
const mic=document.querySelector('#mic');
let lastAnswer='';
let recognition=null;
let installPrompt=null;
function addMessage(text,who,withTools=false){
  const row=document.createElement('div'); row.className=`message-row ${who==='user'?'user-row':'bot-row'}`;
  const avatar=document.createElement('div'); avatar.className='message-avatar'; avatar.textContent=who==='user'?'J':'N';
  const content=document.createElement('div'); content.className='message-content';
  const name=document.createElement('span'); name.className='message-name'; name.textContent=who==='user'?'JOHN SKY':'NOVA AI';
  const time=document.createElement('time'); time.textContent='AGORA'; name.appendChild(time);
  const bubble=document.createElement('div'); bubble.className=`bubble ${who}`; bubble.textContent=text;
  content.append(name,bubble);
  if(withTools){const tools=document.createElement('div');tools.className='message-tools';const btn=document.createElement('button');btn.className='listen-button';btn.type='button';btn.textContent='▶ Ouvir resposta';btn.addEventListener('click',()=>speakText(text));tools.append(btn);content.append(tools);}
  row.append(avatar,content);messages.append(row);messages.scrollTop=messages.scrollHeight;return bubble;
}
function limparParaVoz(texto) {
  return texto
    .replace(/\*\*/g, '')
    .replace(/##+/g, '')
    .replace(/\*/g, '')
    .replace(/\|/g, ', ')
    .replace(/---/g, '')
    .replace(/_/g, '')
    .replace(/#/g, '')
    .replace(/`+/g, '')
    .replace(/\n/g, '. ');
}

function speakText(text){
  if(!('speechSynthesis' in window)){addMessage('A leitura por voz não é suportada neste navegador.', 'bot');return;}
  window.speechSynthesis.cancel();
  const textoLimpo = limparParaVoz(text);
  const utterance=new SpeechSynthesisUtterance(textoLimpo);
  utterance.lang='pt-PT'; utterance.rate=1;
  window.speechSynthesis.speak(utterance);
}
function updateVoiceState(){voiceState.textContent=autoVoice.checked?'Ligada · a NOVA lê as respostas':'Desligada · modo escrita';document.querySelector('#inputMode').textContent=autoVoice.checked?'VOZ AUTOMÁTICA ATIVA':'MODO ESCRITA';}
autoVoice.addEventListener('change',updateVoiceState);updateVoiceState();
async function sendMessage(text){
  const q=text.trim();if(!q)return;
  addMessage(q,'user');input.value='';
  const waiting=addMessage('A processar o teu pedido...','bot');
  try{
    const response=await fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
    const data=await response.json();if(!response.ok)throw new Error(data.error||'Não foi possível obter resposta.');
    lastAnswer=data.answer||'Sem resposta.';waiting.textContent=lastAnswer;
    const tools=document.createElement('div');tools.className='message-tools';const listen=document.createElement('button');listen.className='listen-button';listen.type='button';listen.textContent='▶ Ouvir resposta';listen.addEventListener('click',()=>speakText(lastAnswer));tools.append(listen);waiting.parentElement.append(tools);
    if(autoVoice.checked)speakText(lastAnswer);
  }catch(error){waiting.textContent='Não foi possível contactar a NOVA. '+error.message;}
}
form.addEventListener('submit',e=>{e.preventDefault();sendMessage(input.value);});
document.querySelectorAll('.nav-item').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));button.classList.add('active');input.value=button.dataset.prompt||'';input.focus();}));
document.querySelector('#clear').addEventListener('click',()=>{window.speechSynthesis?.cancel();messages.innerHTML='';addMessage('Conversa limpa. Estou pronta para um novo pedido.','bot',true);});
document.querySelector('#history').addEventListener('click',async()=>{try{const r=await fetch('/api/history');const data=await r.json();if(!data.length){addMessage('Ainda não existem mensagens guardadas no histórico.','bot');return;}data.slice(-20).forEach(item=>{if(item.role==='user')addMessage(item.content,'user');else addMessage(item.content,'bot',true);});}catch(e){addMessage('Não foi possível carregar o histórico.','bot');}});
const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SpeechRecognition){recognition=new SpeechRecognition();recognition.lang='pt-PT';recognition.interimResults=false;recognition.onresult=e=>{input.value=e.results[0][0].transcript;input.focus();};recognition.onerror=()=>{mic.classList.remove('listening');};recognition.onend=()=>mic.classList.remove('listening');mic.addEventListener('click',()=>{try{recognition.start();mic.classList.add('listening');}catch(e){mic.classList.remove('listening');}});}else{mic.disabled=true;mic.title='Ditado por voz não suportado neste navegador.';}
fetch('/api/status').then(r=>r.json()).then(s=>{document.querySelector('#status').textContent=(s.groq_ready?'IA conectada':'IA por configurar')+' · '+(s.voice_ready?'voz local disponível':'voz do navegador');}).catch(()=>document.querySelector('#status').textContent='Servidor indisponível');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;document.querySelector('#install').hidden=false;});
document.querySelector('#install').addEventListener('click',async()=>{if(!installPrompt)return;installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;document.querySelector('#install').hidden=true;});
if('serviceWorker' in navigator && (location.protocol==='https:'||location.hostname==='localhost'))navigator.serviceWorker.register('/service-worker.js').catch(()=>{});
