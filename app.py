
import os
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
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
    
    # Hier würde die eigentliche API-Abfrage stattfinden
    # Dies ist ein Beispiel - die tatsächliche Implementierung hängt von den verwendeten APIs ab
    response = "Dies ist eine Beispielantwort vom Modell " + model
    
    return jsonify({
        "success": True,
        "response": response
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
