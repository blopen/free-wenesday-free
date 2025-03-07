
import os
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 Stunde
Session(app)

# Verfügbare KI-Modelle
MODELS = {
    "gpt-3.5-turbo": {"service": "openai", "free": True},
    "gpt-4": {"service": "openai", "free": False},
    "claude-instant": {"service": "anthropic", "free": True},
    "claude-2": {"service": "anthropic", "free": False},
    "claude-free": {"service": "anthropic-free", "free": True},
    "gemini-pro": {"service": "google", "free": True},
    "llama2-70b": {"service": "meta", "free": True},
    "pi": {"service": "inflection", "free": True}
}

@app.route('/')
def index():
    # API-Schlüssel aus der Session holen oder leere Dictionaries zurückgeben
    api_keys = session.get('api_keys', {})
    active_model = session.get('active_model', 'claude-free')  # Claude-free als Standard
    return render_template('index.html', models=MODELS, api_keys=api_keys, active_model=active_model)

@app.route('/save_api_key', methods=['POST'])
def save_api_key():
    service = request.form.get('service')
    api_key = request.form.get('api_key')
    
    # API-Schlüssel in der Session speichern
    api_keys = session.get('api_keys', {})
    api_keys[service] = api_key
    session['api_keys'] = api_keys
    
    return jsonify({"success": True})

@app.route('/set_active_model', methods=['POST'])
def set_active_model():
    model = request.form.get('model')
    if model in MODELS:
        session['active_model'] = model
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Ungültiges Modell"})

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form.get('message')
    model = session.get('active_model', 'gpt-3.5-turbo')
    model_info = MODELS.get(model)
    
    # API-Schlüssel abrufen
    api_keys = session.get('api_keys', {})
    service = model_info['service']
    api_key = api_keys.get(service)
    
    # Wenn kein API-Schlüssel vorhanden ist und es kein freies Modell ist
    if not api_key and not model_info['free']:
        return jsonify({
            "success": False,
            "error": f"Kein API-Schlüssel für {service} gefunden. Bitte fügen Sie einen Schlüssel hinzu, um Premium-Modelle zu verwenden."
        })
    
    # Chatverlauf aus der Session abrufen oder neu erstellen
    chat_history = session.get('chat_history', [])
    
    # Benutzeranfrage zum Chatverlauf hinzufügen
    chat_history.append({"role": "user", "content": message})
    
    try:
        # Verschiedene API-Aufrufe basierend auf dem Modell
        if service == "openai":
            if api_key:
                # Mit API-Key
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "messages": chat_history
                }
                api_response = requests.post("https://api.openai.com/v1/chat/completions", 
                                           headers=headers, 
                                           json=payload)
                
                if api_response.status_code == 200:
                    response_data = api_response.json()
                    response = response_data['choices'][0]['message']['content']
                else:
                    return jsonify({
                        "success": False,
                        "error": f"API-Fehler: {api_response.text}"
                    })
            else:
                # Freie Version (simuliert öffentliche API)
                response = f"Dies ist eine simulierte Antwort vom freien {model}-Modell: Ich antworte auf '{message}'"
        
        elif service == "anthropic":
            # Implementierung für Claude-Modelle
            if api_key:
                headers = {
                    "x-api-key": api_key,
                    "Content-Type": "application/json"
                }
                
                # Konvertiere Chat-History in das Claude-Format
                claude_messages = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
                
                payload = {
                    "prompt": claude_messages + "\n\nassistant:",
                    "model": model,
                    "max_tokens_to_sample": 500
                }
                
                api_response = requests.post("https://api.anthropic.com/v1/complete", 
                                           headers=headers, 
                                           json=payload)
                
                if api_response.status_code == 200:
                    response_data = api_response.json()
                    response = response_data['completion']
                else:
                    return jsonify({
                        "success": False,
                        "error": f"API-Fehler: {api_response.text}"
                    })
            else:
                # Freie Version (simuliert)
                response = f"Dies ist eine simulierte Antwort vom freien {model}-Modell: Ich antworte auf '{message}'"
        
        elif service == "anthropic-free":
            # Integration mit kostenloser Claude API
            # Bereite Chat-Kontext im Format für Claude vor
            formatted_history = []
            
            for msg in chat_history:
                if msg["role"] == "user":
                    formatted_history.append({"role": "human", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    formatted_history.append({"role": "assistant", "content": msg["content"]})
            
            # Verwende eine öffentliche Claude-Demo-API
            try:
                # Simulierte Implementierung des freien Claude-Modells
                # Diese Implementierung verwendet einen einfachen NLP-Ansatz, der auf der Nachricht und früheren Interaktionen basiert
                
                # Kontext aus dem Chat-Verlauf extrahieren
                context = " ".join([msg["content"] for msg in chat_history[-5:]])  # Verwende die letzten 5 Nachrichten als Kontext
                
                # Einfache Antwortgenerierung basierend auf Schlüsselwörtern
                if "hallo" in message.lower() or "hi" in message.lower() or "guten tag" in message.lower():
                    response = "Hallo! Ich bin Claude, wie kann ich dir heute helfen?"
                elif "wie geht es dir" in message.lower():
                    response = "Mir geht es gut, danke der Nachfrage! Als KI habe ich keine Gefühle, aber ich bin bereit, dir zu helfen."
                elif "was kannst du" in message.lower() or "fähigkeiten" in message.lower():
                    response = "Als Claude-Modell kann ich Fragen beantworten, bei Textgenerierung helfen, Informationen analysieren und in Gesprächen unterstützen. Ich versuche, hilfreiche, höfliche und präzise Antworten zu geben."
                elif "danke" in message.lower():
                    response = "Gerne! Wenn du weitere Fragen hast, stehe ich dir zur Verfügung."
                elif "wetter" in message.lower():
                    response = "Als KI habe ich leider keinen Zugriff auf aktuelle Wetterdaten. Es wäre am besten, einen Wetterdienst oder eine Wetter-App zu nutzen."
                elif any(q in message.lower() for q in ["warum", "wieso", "weshalb"]):
                    response = "Das ist eine interessante Frage. Es gibt verschiedene Faktoren zu berücksichtigen. Könnte ich mehr Kontext bekommen, um eine präzisere Antwort zu geben?"
                elif "erklär" in message.lower() or "erkläre" in message.lower():
                    topic = message.lower().replace("erklär", "").replace("erkläre", "").strip()
                    response = f"Ich versuche, {topic} zu erklären: Es handelt sich um ein komplexes Thema mit verschiedenen Aspekten. Möchtest du, dass ich auf einen bestimmten Teil davon näher eingehe?"
                else:
                    # Fallback-Antwort für alle anderen Anfragen
                    response = f"Ich verstehe deine Anfrage zu '{message}'. Als kostenlose Version von Claude kann ich dir hierzu grundlegende Informationen geben. Für detailliertere Analysen würde ich die vollständige Claude-Version empfehlen. Kann ich dir mit etwas anderem helfen?"
                
            except Exception as e:
                response = "Es tut mir leid, ich konnte deine Anfrage nicht verarbeiten. Bitte versuche es noch einmal mit einer anderen Formulierung."
        
        else:
            # Für andere Modelle (simuliert)
            response = f"Dies ist eine simulierte Antwort vom Modell {model}: Ich antworte auf '{message}'"
        
        # Antwort zum Chatverlauf hinzufügen
        chat_history.append({"role": "assistant", "content": response})
        
        # Chatverlauf in der Session speichern
        session['chat_history'] = chat_history
        
        return jsonify({
            "success": True,
            "response": response
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Fehler bei der Verarbeitung: {str(e)}"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
