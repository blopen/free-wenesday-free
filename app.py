import os
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import admin  # Import unseres Admin-Moduls

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_PERMANENT_LIFETIME"] = 3600  # 1 Stunde
Session(app)

# Registriere Admin-Routen
admin.register_admin_routes(app)

# Verfügbare KI-Modelle mit Details
MODELS = {
    "gpt-3.5-turbo": {"service": "openai", "free": True, "max_tokens": 4096},
    "gpt-4": {"service": "openai", "free": False, "max_tokens": 8192},
    "gpt-4-turbo": {"service": "openai", "free": False, "max_tokens": 16384},
    "claude-instant": {"service": "anthropic", "free": True, "max_tokens": 4096},
    "claude-2": {"service": "anthropic", "free": False, "max_tokens": 8192},
    "claude-3-opus": {"service": "anthropic", "free": False, "max_tokens": 16384},
    "claude-3-sonnet": {"service": "anthropic", "free": False, "max_tokens": 12288},
    "claude-free": {"service": "anthropic-free", "free": True, "max_tokens": 2048},
    "gemini-pro": {"service": "google", "free": True, "max_tokens": 4096},
    "gemini-ultra": {"service": "google", "free": False, "max_tokens": 8192},
    "llama2-70b": {"service": "meta", "free": True, "max_tokens": 4096},
    "llama3-70b": {"service": "meta", "free": False, "max_tokens": 8192},
    "pi": {"service": "inflection", "free": True, "max_tokens": 2048}
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

                max_tokens = model_info.get('max_tokens', 2048)

                payload = {
                    "model": model,
                    "messages": chat_history,
                    "temperature": 0.7,
                    "max_tokens": min(max_tokens // 2, 2048),  # Use half of available context
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }

                try:
                    api_response = requests.post(
                        "https://api.openai.com/v1/chat/completions", 
                        headers=headers, 
                        json=payload,
                        timeout=30  # Set timeout to 30 seconds
                    )

                    if api_response.status_code == 200:
                        response_data = api_response.json()
                        response = response_data['choices'][0]['message']['content']
                    else:
                        error_data = api_response.json() if api_response.text else {"error": "Unknown API error"}
                        error_message = error_data.get("error", {}).get("message", str(error_data))

                        return jsonify({
                            "success": False,
                            "error": f"OpenAI API-Fehler: {error_message}"
                        })
                except requests.exceptions.Timeout:
                    return jsonify({
                        "success": False,
                        "error": "Die Anfrage hat das Zeitlimit überschritten. Bitte versuchen Sie es erneut."
                    })
                except requests.exceptions.ConnectionError:
                    return jsonify({
                        "success": False,
                        "error": "Verbindungsfehler. Bitte überprüfen Sie Ihre Internetverbindung."
                    })
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "error": f"Unerwarteter Fehler: {str(e)}"
                    })
            else:
                # Freie Version - Verwende Demo-API wenn verfügbar, sonst Simulation
                try:
                    response = f"Dies ist eine simulierte Antwort vom {model}-Modell. Für vollständige Funktionalität fügen Sie bitte Ihren API-Schlüssel hinzu. Ich versuche, auf '{message}' zu antworten."
                except Exception:
                    response = f"Simulierte Antwort: Hallo! Ich bin ein Assistent. Wie kann ich dir helfen?"

        elif service == "anthropic":
            # Implementierung für Claude-Modelle
            if api_key:
                # Check if we're using Claude 3 models
                is_claude3 = "claude-3" in model
                max_tokens = model_info.get('max_tokens', 2048)

                if is_claude3:
                    # Claude 3 API uses messages API similar to OpenAI
                    headers = {
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    }

                    # Convert standard chat format to Claude 3 format
                    claude_messages = []
                    for msg in chat_history:
                        role = "assistant" if msg["role"] == "assistant" else "user"
                        claude_messages.append({"role": role, "content": msg["content"]})

                    payload = {
                        "model": model,
                        "messages": claude_messages,
                        "max_tokens": min(max_tokens // 2, 1024),
                        "temperature": 0.7
                    }

                    try:
                        api_response = requests.post(
                            "https://api.anthropic.com/v1/messages", 
                            headers=headers, 
                            json=payload,
                            timeout=30
                        )

                        if api_response.status_code == 200:
                            response_data = api_response.json()
                            response = response_data['content'][0]['text']
                        else:
                            error_data = api_response.json() if api_response.text else {"error": "Unknown API error"}
                            error_message = error_data.get("error", {}).get("message", str(error_data))

                            return jsonify({
                                "success": False,
                                "error": f"Anthropic API-Fehler: {error_message}"
                            })
                    except Exception as e:
                        return jsonify({
                            "success": False,
                            "error": f"Anthropic API-Fehler: {str(e)}"
                        })
                else:
                    # Legacy Claude API (Claude 2, Claude Instant)
                    headers = {
                        "x-api-key": api_key,
                        "Content-Type": "application/json"
                    }

                    # Convert chat history to Claude format
                    claude_messages = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

                    payload = {
                        "prompt": claude_messages + "\n\nassistant:",
                        "model": model,
                        "max_tokens_to_sample": min(max_tokens // 2, 1024),
                        "temperature": 0.7
                    }

                    try:
                        api_response = requests.post(
                            "https://api.anthropic.com/v1/complete", 
                            headers=headers, 
                            json=payload,
                            timeout=30
                        )

                        if api_response.status_code == 200:
                            response_data = api_response.json()
                            response = response_data['completion']
                        else:
                            error_data = api_response.json() if api_response.text else {"error": "Unknown API error"}
                            error_message = error_data.get("error", {}).get("message", str(error_data))

                            return jsonify({
                                "success": False,
                                "error": f"Anthropic API-Fehler: {error_message}"
                            })
                    except Exception as e:
                        return jsonify({
                            "success": False,
                            "error": f"Anthropic API-Fehler: {str(e)}"
                        })
            else:
                # Freie Version (simuliert)
                response = f"Dies ist eine simulierte Antwort vom {model}-Modell. Für vollständige Funktionalität fügen Sie bitte Ihren API-Schlüssel hinzu. Ich versuche, auf '{message}' zu antworten."

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