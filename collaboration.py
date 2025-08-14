import os
import uuid
import requests
from flask import Blueprint, request, jsonify

# Blueprint for collaborative chat sessions
collab_bp = Blueprint('collab', __name__)

# In-memory store for chat sessions: {session_id: [messages]}
collab_sessions = {}

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@collab_bp.route('/collab/create', methods=['POST'])
def create_session():
    """Create a new collaborative chat session and return its ID."""
    session_id = str(uuid.uuid4())
    collab_sessions[session_id] = []
    return jsonify({"session_id": session_id})

@collab_bp.route('/collab/<session_id>/chat', methods=['POST'])
def collab_chat(session_id):
    """Send a message within a collaborative session and get GPT-4 response."""
    data = request.get_json(silent=True) or request.form
    message = data.get('message') if data else None
    if not message:
        return jsonify({"success": False, "error": "No message provided"}), 400

    history = collab_sessions.setdefault(session_id, [])
    history.append({"role": "user", "content": message})

    if not OPENAI_API_KEY:
        return jsonify({"success": False, "error": "Server missing OPENAI_API_KEY"}), 500

    payload = {
        "model": "gpt-4-turbo",
        "messages": history,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    api_response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    if api_response.status_code == 200:
        response_data = api_response.json()
        ai_message = response_data['choices'][0]['message']['content']
        history.append({"role": "assistant", "content": ai_message})
        return jsonify({"success": True, "response": ai_message, "history": history})
    else:
        error = api_response.json().get('error', {}).get('message', 'Unknown error')
        return jsonify({"success": False, "error": error}), 500

@collab_bp.route('/collab/<session_id>/history', methods=['GET'])
def get_history(session_id):
    """Retrieve the current chat history for a collaborative session."""
    return jsonify(collab_sessions.get(session_id, []))

