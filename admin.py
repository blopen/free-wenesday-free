
import os
import json
from flask import session, redirect, url_for, render_template, request, jsonify

# Datei für die Berechtigungen
PERMISSIONS_FILE = 'model_permissions.json'

def init_permissions():
    """Initialisiert die Berechtigungsdatei, falls sie nicht existiert"""
    if not os.path.exists(PERMISSIONS_FILE):
        default_permissions = {
            "default": {
                "free_models": ["gpt-3.5-turbo", "claude-instant", "claude-free", "gemini-pro", "llama2-70b"],
                "premium_models": ["gpt-4", "gpt-4-turbo", "claude-2", "claude-3-opus", "claude-3-sonnet", "gemini-ultra", "llama3-70b"]
            },
            "users": {}
        }
        save_permissions(default_permissions)
        return default_permissions
    return load_permissions()

def load_permissions():
    """Lädt die Berechtigungen aus der Datei"""
    try:
        with open(PERMISSIONS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return init_permissions()

def save_permissions(permissions):
    """Speichert die Berechtigungen in der Datei"""
    with open(PERMISSIONS_FILE, 'w') as f:
        json.dump(permissions, f, indent=4)

def get_user_permissions(user_id):
    """Gibt die Berechtigungen eines Benutzers zurück"""
    permissions = load_permissions()
    if user_id in permissions["users"]:
        return permissions["users"][user_id]
    return permissions["default"]

def is_admin(user_id):
    """Prüft, ob ein Benutzer Admin-Rechte hat"""
    permissions = load_permissions()
    user_data = permissions["users"].get(user_id, {})
    return user_data.get("is_admin", False)

def get_available_models(user_id):
    """Gibt die für einen Benutzer verfügbaren Modelle zurück"""
    user_permissions = get_user_permissions(user_id)
    available_models = user_permissions.get("free_models", [])
    
    if user_permissions.get("has_premium", False):
        available_models.extend(user_permissions.get("premium_models", []))
    
    return available_models

def set_user_permission(user_id, permission_type, models):
    """Setzt Benutzerberechtigungen für bestimmte Modelltypen"""
    permissions = load_permissions()
    
    if user_id not in permissions["users"]:
        permissions["users"][user_id] = {
            "free_models": permissions["default"]["free_models"].copy(),
            "premium_models": permissions["default"]["premium_models"].copy(),
            "has_premium": False,
            "is_admin": False
        }
    
    permissions["users"][user_id][permission_type] = models
    save_permissions(permissions)
    return True

def set_user_premium_access(user_id, has_premium):
    """Setzt den Premium-Zugriff für einen Benutzer"""
    permissions = load_permissions()
    
    if user_id not in permissions["users"]:
        permissions["users"][user_id] = {
            "free_models": permissions["default"]["free_models"].copy(),
            "premium_models": permissions["default"]["premium_models"].copy(),
            "has_premium": False,
            "is_admin": False
        }
    
    permissions["users"][user_id]["has_premium"] = has_premium
    save_permissions(permissions)
    return True

def set_user_admin_status(user_id, is_admin_status):
    """Setzt den Admin-Status für einen Benutzer"""
    permissions = load_permissions()
    
    if user_id not in permissions["users"]:
        permissions["users"][user_id] = {
            "free_models": permissions["default"]["free_models"].copy(),
            "premium_models": permissions["default"]["premium_models"].copy(),
            "has_premium": False,
            "is_admin": False
        }
    
    permissions["users"][user_id]["is_admin"] = is_admin_status
    save_permissions(permissions)
    return True

def get_all_users():
    """Gibt alle Benutzer mit ihren Berechtigungen zurück"""
    permissions = load_permissions()
    return permissions["users"]

# Admin-Routen für die Flask-Anwendung
def register_admin_routes(app):
    @app.route('/admin/login_as_admin', methods=['POST'])
    def login_as_admin():
        # Dummy-Admin-ID erstellen und im Session-Objekt speichern
        dummy_admin_id = "admin_user_12345"
        session['user_id'] = dummy_admin_id
        
        # Prüfen, ob der Admin bereits in der Berechtigungsliste existiert
        permissions = load_permissions()
        if dummy_admin_id not in permissions["users"]:
            # Admin-Benutzer mit allen Rechten erstellen
            permissions["users"][dummy_admin_id] = {
                "free_models": permissions["default"]["free_models"].copy(),
                "premium_models": permissions["default"]["premium_models"].copy(),
                "has_premium": True,
                "is_admin": True
            }
            save_permissions(permissions)
        
        return jsonify({"success": True})
    
    @app.route('/admin')
    def admin_dashboard():
        # Holen Sie die User-ID aus der Session (falls verfügbar) oder aus den Headers
        user_id = session.get('user_id') or request.headers.get('X-Replit-User-Id')
        if not user_id or not is_admin(user_id):
            return redirect(url_for('index'))
        
        users = get_all_users()
        all_permissions = load_permissions()
        default_models = all_permissions["default"]
        
        return render_template(
            'admin.html',
            users=users,
            default_models=default_models,
            user_id=user_id,
            user_name=session.get('user_name', 'Admin')
        )
    
    @app.route('/admin/user/<user_id>', methods=['GET'])
    def admin_user_details(user_id):
        admin_id = request.headers.get('X-Replit-User-Id')
        if not admin_id or not is_admin(admin_id):
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        
        user_permissions = get_user_permissions(user_id)
        all_permissions = load_permissions()
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "permissions": user_permissions,
            "default_models": all_permissions["default"]
        })
    
    @app.route('/admin/user/<user_id>/update', methods=['POST'])
    def admin_update_user(user_id):
        admin_id = request.headers.get('X-Replit-User-Id')
        if not admin_id or not is_admin(admin_id):
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        
        data = request.json
        if "free_models" in data:
            set_user_permission(user_id, "free_models", data["free_models"])
        
        if "premium_models" in data:
            set_user_permission(user_id, "premium_models", data["premium_models"])
        
        if "has_premium" in data:
            set_user_premium_access(user_id, data["has_premium"])
        
        if "is_admin" in data:
            set_user_admin_status(user_id, data["is_admin"])
        
        return jsonify({"success": True})
    
    @app.route('/admin/default/update', methods=['POST'])
    def admin_update_default():
        admin_id = request.headers.get('X-Replit-User-Id')
        if not admin_id or not is_admin(admin_id):
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        
        data = request.json
        permissions = load_permissions()
        
        if "free_models" in data:
            permissions["default"]["free_models"] = data["free_models"]
        
        if "premium_models" in data:
            permissions["default"]["premium_models"] = data["premium_models"]
        
        save_permissions(permissions)
        return jsonify({"success": True})
    
    @app.route('/api/available_models')
    def get_models():
        user_id = request.headers.get('X-Replit-User-Id')
        if not user_id:
            # Für nicht angemeldete Benutzer nur freie Modelle zurückgeben
            default_permissions = load_permissions()["default"]
            return jsonify({
                "success": True,
                "models": default_permissions["free_models"],
                "is_admin": False,
                "has_premium": False
            })
        
        user_permissions = get_user_permissions(user_id)
        available_models = user_permissions.get("free_models", [])
        
        has_premium = user_permissions.get("has_premium", False)
        if has_premium:
            available_models.extend(user_permissions.get("premium_models", []))
        
        return jsonify({
            "success": True,
            "models": available_models,
            "is_admin": is_admin(user_id),
            "has_premium": has_premium
        })
