
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json
import os

# Datei für die Benutzer
USERS_FILE = 'users.json'

def init_users_file():
    """Initialisiert die Benutzerdatei, falls sie nicht existiert"""
    if not os.path.exists(USERS_FILE):
        default_users = {
            "users": {}
        }
        save_users(default_users)
        return default_users
    return load_users()

def load_users():
    """Lädt die Benutzer aus der Datei"""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return init_users_file()

def save_users(users):
    """Speichert die Benutzer in der Datei"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

class User(UserMixin):
    def __init__(self, id, email, name, password_hash=None, google_id=None, created_at=None, is_admin=False):
        self.id = id
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.google_id = google_id
        self.created_at = created_at or datetime.datetime.now().isoformat()
        self.is_admin = is_admin
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'password_hash': self.password_hash,
            'google_id': self.google_id,
            'created_at': self.created_at,
            'is_admin': self.is_admin
        }
    
    @classmethod
    def get(cls, user_id):
        users = load_users()
        user_data = users.get('users', {}).get(user_id)
        if user_data:
            return cls(
                id=user_id,
                email=user_data.get('email'),
                name=user_data.get('name'),
                password_hash=user_data.get('password_hash'),
                google_id=user_data.get('google_id'),
                created_at=user_data.get('created_at'),
                is_admin=user_data.get('is_admin', False)
            )
        return None
    
    @classmethod
    def find_by_email(cls, email):
        users = load_users()
        for user_id, user_data in users.get('users', {}).items():
            if user_data.get('email') == email:
                return cls(
                    id=user_id,
                    email=user_data.get('email'),
                    name=user_data.get('name'),
                    password_hash=user_data.get('password_hash'),
                    google_id=user_data.get('google_id'),
                    created_at=user_data.get('created_at'),
                    is_admin=user_data.get('is_admin', False)
                )
        return None
    
    @classmethod
    def find_by_google_id(cls, google_id):
        users = load_users()
        for user_id, user_data in users.get('users', {}).items():
            if user_data.get('google_id') == google_id:
                return cls(
                    id=user_id,
                    email=user_data.get('email'),
                    name=user_data.get('name'),
                    password_hash=user_data.get('password_hash'),
                    google_id=user_data.get('google_id'),
                    created_at=user_data.get('created_at'),
                    is_admin=user_data.get('is_admin', False)
                )
        return None
    
    def save(self):
        users = load_users()
        users.setdefault('users', {})[self.id] = self.to_dict()
        save_users(users)
