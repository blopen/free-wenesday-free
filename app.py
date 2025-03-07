
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
    "gemini-pro": {"service": "google", "free": True},
    "llama2-70b": {"service": "meta", "free": True},
    "pi": {"service": "inflection", "free": True}
}

@app.route('/')
def index():
    # API-Schlüssel aus der Session holen oder leere Dictionaries zurückgeben
    api_keys = session.get('api_keys', {})
    active_model = session.get('active_model', 'gpt-3.5-turbo')
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
