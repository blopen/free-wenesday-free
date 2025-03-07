import os
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import admin  # Import unseres Admin-Moduls
from app_config import MODEL_PROXY_URLS, FREE_MODEL_RATE_LIMITS  # Import der Konfiguration

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
    
    # Prüfen, ob der Benutzer Admin-Rechte hat
    user_id = session.get('user_id') or request.headers.get('X-Replit-User-Id')
    is_admin_user = admin.is_admin(user_id) if user_id else False
    
    return render_template('index.html', models=MODELS, api_keys=api_keys, active_model=active_model, is_admin=is_admin_user)

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
                # Freie Version - Verwende Proxy-API
                proxy_url = MODEL_PROXY_URLS.get(model)
                
                if proxy_url:
                    try:
                        # Versuch, das öffentliche Proxy-API zu nutzen
                        headers = {
                            "Content-Type": "application/json",
                            "X-Proxy-Request": "true"
                        }
                        
                        payload = {
                            "messages": chat_history,
                            "message": message
                        }
                        
                        # Versuche, die öffentliche API über den Server anzusprechen
                        api_response = requests.post(
                            proxy_url,
                            headers=headers,
                            json=payload,
                            timeout=5
                        )
                        
                        if api_response.status_code == 200:
                            response_data = api_response.json()
                            response = response_data.get('response', "Die API ist momentan nicht erreichbar. Der Client-seitige Proxy wird versuchen, eine Antwort zu erhalten.")
                        else:
                            # Falls Server-Proxy fehlschlägt, Fallback auf Client-seitigen Proxy
                            response = "Das freie Modell kann nicht über den Server erreicht werden. Der Client-seitige Proxy wird verwendet. Bitte warten Sie einen Moment..."
                    
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        # Timeout oder Verbindungsfehler
                        response = "Server-Timeout beim Versuch, das Modell zu erreichen. Der Client-seitige Proxy wird verwendet. Bitte warten Sie einen Moment..."
                    
                    except Exception as e:
                        response = f"Fehler beim Zugriff auf die öffentliche API: {str(e)}. Der Client-seitige Proxy wird versuchen, eine Antwort zu erhalten."
                else:
                    # Kein Proxy-URL für dieses Modell konfiguriert
                    response = f"Für das Modell {model} ist kein öffentlicher Proxy konfiguriert. Bitte wählen Sie ein anderes Modell oder fügen Sie Ihren API-Schlüssel hinzu."

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
            # Integration mit kostenloser Claude API über Proxy
            # Bereite Chat-Kontext im Format für Claude vor
            formatted_history = []

            for msg in chat_history:
                if msg["role"] == "user":
                    formatted_history.append({"role": "human", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    formatted_history.append({"role": "assistant", "content": msg["content"]})

            # Get proxy URL from config
            proxy_url = MODEL_PROXY_URLS.get(model)
            
            if proxy_url:
                try:
                    # Versuch, das öffentliche Proxy-API zu nutzen
                    headers = {
                        "Content-Type": "application/json",
                        "X-Proxy-Request": "true"
                    }
                    
                    payload = {
                        "messages": formatted_history,
                        "message": message
                    }
                    
                    # Versuche, die öffentliche API über den Server anzusprechen
                    api_response = requests.post(
                        proxy_url,
                        headers=headers,
                        json=payload,
                        timeout=5  # Kurzes Timeout, da der Client direkten Proxy nutzen soll
                    )
                    
                    if api_response.status_code == 200:
                        response_data = api_response.json()
                        response = response_data.get('response', "Die API ist momentan nicht erreichbar. Bitte versuchen Sie es später erneut.")
                    else:
                        # Falls Server-Proxy fehlschlägt, Fallback auf Client-seitigen Proxy
                        response = "Das freie Modell kann nicht über den Server erreicht werden. Der Client-seitige Proxy wird verwendet. Bitte warten Sie einen Moment..."
                
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    # Timeout oder Verbindungsfehler - Client-seitigen Proxy verwenden
                    response = "Server-Timeout beim Versuch, das Modell zu erreichen. Der Client-seitige Proxy wird verwendet. Bitte warten Sie einen Moment..."
                
                except Exception as e:
                    response = f"Fehler beim Zugriff auf die öffentliche API: {str(e)}. Der Client-seitige Proxy wird versuchen, eine Antwort zu erhalten."
            else:
                # Kein Proxy-URL für dieses Modell konfiguriert
                response = f"Für das Modell {model} ist kein öffentlicher Proxy konfiguriert. Bitte wählen Sie ein anderes Modell oder fügen Sie Ihren API-Schlüssel hinzu."

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
# Import für DeepSeek-AI
try:
    import deepseek
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False
    print("DeepSeek-AI nicht verfügbar. Bitte installieren Sie es mit: pip install deepseek-ai")

# Offline-Modell-Integration
@app.route('/offline_model_request', methods=['POST'])
def offline_model_request():
    if not DEEPSEEK_AVAILABLE:
        # Einfache Simulation, wenn DeepSeek nicht verfügbar ist
        data = request.get_json()
        message = data.get('message', '')
        
        # Einfache Antwort generieren
        simulated_response = f"Als Offline-Fallback-Modell kann ich einfache Anfragen beantworten. Sie haben gefragt: '{message}'. Leider ist das echte DeepSeek-Modell nicht installiert, aber ich versuche zu helfen."
        
        return jsonify({
            "success": True,
            "response": simulated_response
        })
        
    data = request.get_json()
    message = data.get('message', '')
    model_name = data.get('model', 'deepseek-chat')
    
    try:
        # DeepSeek-Modell initialisieren und Antwort generieren
        if model_name == 'deepseek-coder':
            model = deepseek.CodeModel()
        else:
            model = deepseek.ChatModel()
            
        response = model.generate(message, max_tokens=1024)
        
        return jsonify({
            "success": True,
            "response": response
        })
    except Exception as e:
        # Fehlerbehandlung mit Fallback-Antwort
        fallback_response = f"Es gab ein Problem mit dem Offline-Modell. Ihre Anfrage war: '{message}'. Leider kann ich darauf im Moment nicht richtig antworten. Fehler: {str(e)}"
        
        return jsonify({
            "success": True,  # Senden "success: true" um die UI flüssig zu halten
            "response": fallback_response
        })
