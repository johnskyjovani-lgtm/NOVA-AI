import os, threading, webbrowser
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from nova.assistant import NovaAssistant
from nova.database import init_db, save_message, recent_messages
load_dotenv(); BASE=Path(__file__).resolve().parent; DB=BASE/'nova.db'
WORK=(BASE/os.getenv('NOVA_WORKSPACE','workspace')).resolve(); WORK.mkdir(exist_ok=True)
init_db(DB); nova=NovaAssistant(WORK); web=Flask(__name__, static_folder=str(BASE/'nova'/'static'), static_url_path='')
@web.get('/')
def home(): return send_from_directory(BASE/'nova'/'static','index.html')
@web.get('/manifest.json')
def manifest(): return send_from_directory(BASE/'nova'/'static','manifest.json',mimetype='application/manifest+json')
@web.get('/service-worker.js')
def service_worker(): return send_from_directory(BASE/'nova'/'static','service-worker.js',mimetype='application/javascript')
@web.get('/api/status')
def status(): return jsonify(groq_ready=bool(nova.client),voice_ready=nova.voice_ready,creator='John Sky',brand='JOHN SKY DESIGN')
@web.get('/api/history')
def history(): return jsonify(recent_messages(DB))
@web.post('/api/ask')
def ask():
    prompt=str(request.get_json(force=True).get('message','')).strip()
    if not prompt: return jsonify(error='Escreve um pedido.'),400
    answer=nova.handle(prompt); save_message(DB,'user',prompt); save_message(DB,'assistant',answer)
    return jsonify(answer=answer)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
